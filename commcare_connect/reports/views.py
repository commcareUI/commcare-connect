from datetime import date, datetime

import django_filters
import django_tables2 as tables
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from django.db.models import Max, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django_filters.views import FilterView

from commcare_connect.opportunity.models import CompletedWork, CompletedWorkStatus, DeliveryType, Payment

from .tables import AdminReportTable

ADMIN_REPORT_START = (2023, 1)


def _increment(quarter):
    year, q = quarter
    if q < 4:
        q += 1
    else:
        year += 1
        q = 1
    return (year, q)


def _get_quarters_since_start():
    today = date.today()
    current_quarter = (today.year, (today.month - 1) // 3 + 1)
    quarters = []
    q = ADMIN_REPORT_START
    while q <= current_quarter:
        quarters.append(q)
        q = _increment(q)
    return quarters


def _get_table_data_for_quarter(quarter, delivery_type):
    if delivery_type:
        delivery_type_filter = Q(opportunity_access__opportunity__delivery_type__slug=delivery_type)
    else:
        delivery_type_filter = Q()

    quarter_start = date(quarter[0], (quarter[1] - 1) * 3 + 1, 1)
    next_quarter = _increment(quarter)
    quarter_end = date(next_quarter[0], (next_quarter[1] - 1) * 3 + 1, 1)

    user_set = set()
    beneficiary_set = set()
    service_count = 0
    last_pk = 0
    more = True

    while more:
        visit_data = (
            CompletedWork.objects.annotate(work_date=Max("uservisit__visit_date"))
            .filter(
                delivery_type_filter,
                opportunity_access__opportunity__is_test=False,
                status=CompletedWorkStatus.approved,
                work_date__gte=quarter_start,
                work_date__lt=quarter_end,
                id__gt=last_pk,
            )
            .select_related("opportunity_access")
        ).order_by("id")[:100]

        if len(visit_data) < 100:
            more = False
        for v in visit_data:
            user_set.add(v.opportunity_access.user_id)
            beneficiary_set.add(v.entity_id)
            service_count += v.approved_count
            last_pk = v.id

    approved_payment_amount = (
        Payment.objects.filter(
            delivery_type_filter,
            opportunity_access__opportunity__is_test=False,
            confirmed=True,
            date_paid__gte=quarter_start,
            date_paid__lt=quarter_end,
        ).aggregate(Sum("amount_usd"))
    )["amount_usd__sum"]

    total_payment_amount = (
        Payment.objects.filter(
            delivery_type_filter,
            opportunity_access__opportunity__is_test=False,
            date_paid__gte=quarter_start,
            date_paid__lt=quarter_end,
        ).aggregate(Sum("amount_usd"))
    )["amount_usd__sum"]

    return {
        "quarter": f"{quarter[0]} Q{quarter[1]}",
        "users": len(user_set),
        "services": service_count,
        "approved_payments": approved_payment_amount,
        "total_payments": total_payment_amount,
        "beneficiaries": len(beneficiary_set),
    }


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_GET
def program_dashboard_report(request):
    return render(
        request,
        "reports/dashboard.html",
        context={"mapbox_token": settings.MAPBOX_TOKEN},
    )


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_GET
def visit_map_data(request):
    with connection.cursor() as cursor:
        # Read the SQL file
        with open("commcare_connect/reports/sql/visit_map.sql") as sql_file:
            sql_query = sql_file.read()

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all results
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Convert to GeoJSON
    geojson = _results_to_geojson(results)

    # Return the GeoJSON as JSON response
    return JsonResponse(geojson, safe=False)


def _results_to_geojson(results):
    geojson = {"type": "FeatureCollection", "features": []}
    status_to_color = {
        "approved": "#00FF00",
        "rejected": "#FF0000",
    }
    for result in results:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(result["gps_location_long"]), float(result["gps_location_lat"])],
            },
            "properties": {
                key: value for key, value in result.items() if key not in ["gps_location_lat", "gps_location_long"]
            },
        }
        color = status_to_color.get(result["status"], "#FFFF00")
        feature["properties"]["color"] = color
        geojson["features"].append(feature)

    return geojson


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class DeliveryReportFilters(django_filters.FilterSet):
    delivery_type = django_filters.ChoiceFilter(method="filter_by_ignore")
    year = django_filters.ChoiceFilter(method="filter_by_ignore")
    quarter = django_filters.ChoiceFilter(
        choices=[(1, "Q1"), (2, "Q2"), (3, "Q3"), (4, "Q4")], label="Quarter", method="filter_by_ignore"
    )
    by_delivery_type = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(),
        label='Break up by delivery type',
        method='filter_by_ignore'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.now().year
        year_choices = [(year, str(year)) for year in range(2023, current_year + 1)]
        self.filters["year"] = django_filters.ChoiceFilter(
            choices=year_choices, label="Year", method="filter_by_ignore"
        )

        delivery_types = DeliveryType.objects.values_list("slug", "name")
        self.filters["delivery_type"] = django_filters.ChoiceFilter(choices=delivery_types, label="Delivery Type")

    def filter_by_ignore(self, queryset, name, value):
        return queryset

    class Meta:
        model = None
        fields = ["delivery_type", "year", "quarter", "by_delivery_type"]
        unknown_field_behavior = django_filters.UnknownFieldBehavior.IGNORE


class NonModelFilterView(FilterView):
    def get_queryset(self):
        # Doesn't matter which model it is here
        return CompletedWork.objects.none()

    @property
    def object_list(self):
        # Override this
        return []

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        context = self.get_context_data(filter=self.filterset, object_list=self.object_list)
        return self.render_to_response(context)


class DeliveryStatsReportView(tables.SingleTableMixin, SuperUserRequiredMixin, NonModelFilterView):
    table_class = AdminReportTable
    filterset_class = DeliveryReportFilters

    def get_template_names(self):
        if self.request.htmx:
            template_name = "reports/htmx_table.html"
        else:
            template_name = "reports/report_table.html"

        return template_name

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_url"] = reverse("reports:delivery_stats_report")
        return context

    @property
    def object_list(self):
        table_data = []
        if not self.filterset.form.is_valid():
            return []

        filter_values = self.filterset.form.cleaned_data
        delivery_type = filter_values["delivery_type"]
        year = int(filter_values["year"])
        quarter = filter_values["quarter"]

        if not year:
            quarters = _get_quarters_since_start()
        elif year:
            if quarter:
                quarters = [(year, int(quarter))]
            else:
                quarters = [(year, q) for q in range(1, 5)]

        for q in quarters:
            data = _get_table_data_for_quarter(q, delivery_type)
            table_data.append(data)
        return table_data
