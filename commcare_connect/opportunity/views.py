import datetime
import json
from collections import namedtuple
from functools import reduce

from celery.result import AsyncResult
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import storages
from django.db.models import F, Q
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.timezone import now
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_tables2 import SingleTableView
from django_tables2.export import TableExport
from geopy import distance

from commcare_connect.form_receiver.serializers import XFormSerializer
from commcare_connect.opportunity.api.serializers import remove_opportunity_access_cache
from commcare_connect.opportunity.forms import (
    AddBudgetExistingUsersForm,
    DateRanges,
    OpportunityChangeForm,
    OpportunityCreationForm,
    OpportunityFinalizeForm,
    OpportunityInitForm,
    OpportunityVerificationFlagsConfigForm,
    PaymentExportForm,
    PaymentUnitForm,
    SendMessageMobileUsersForm,
    VisitExportForm,
)
from commcare_connect.opportunity.helpers import (
    get_annotated_opportunity_access,
    get_annotated_opportunity_access_deliver_status,
)
from commcare_connect.opportunity.models import (
    BlobMeta,
    CatchmentArea,
    CompletedWork,
    CompletedWorkStatus,
    DeliverUnit,
    Opportunity,
    OpportunityAccess,
    OpportunityClaim,
    OpportunityClaimLimit,
    OpportunityVerificationFlags,
    Payment,
    PaymentUnit,
    UserVisit,
    VisitValidationStatus,
)
from commcare_connect.opportunity.tables import (
    CompletedWorkTable,
    DeliverStatusTable,
    LearnStatusTable,
    OpportunityPaymentTable,
    PaymentReportTable,
    PaymentUnitTable,
    SuspendedUsersTable,
    UserPaymentsTable,
    UserStatusTable,
    UserVisitReviewTable,
    UserVisitTable,
)
from commcare_connect.opportunity.tasks import (
    add_connect_users,
    create_learn_modules_and_deliver_units,
    generate_catchment_area_export,
    generate_deliver_status_export,
    generate_payment_export,
    generate_user_status_export,
    generate_visit_export,
    generate_work_status_export,
    send_push_notification_task,
    send_sms_task,
)
from commcare_connect.opportunity.visit_import import (
    ImportException,
    bulk_update_catchments,
    bulk_update_completed_work_status,
    bulk_update_payment_status,
    bulk_update_visit_status,
    update_payment_accrued,
)
from commcare_connect.organization.decorators import org_admin_required, org_member_required, org_viewer_required
from commcare_connect.program.models import (
    ManagedOpportunity,
    ManagedOpportunityApplication,
    ManagedOpportunityApplicationStatus,
)
from commcare_connect.users.models import User
from commcare_connect.utils.commcarehq_api import get_applications_for_user_by_domain, get_domains_for_user


class OrganizationUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # request.org_membership is a SimpleLazyObject object so `is not None` is always `True`
        return self.request.org_membership != None or self.request.user.is_superuser  # noqa: E711


class OrganizationUserMemberRoleMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.org_membership != None and not self.request.org_membership.is_viewer  # noqa: E711
        ) or self.request.user.is_superuser


def get_opportunity_or_404(pk, org_slug):
    opp = get_object_or_404(Opportunity, id=pk)

    if (opp.organization and opp.organization.slug == org_slug) or (
        opp.managed and opp.managedopportunity.program.organization.slug == org_slug
    ):
        return opp

    raise Http404("Opportunity not found.")


class OpportunityList(OrganizationUserMixin, ListView):
    model = Opportunity
    paginate_by = 10

    def get_queryset(self):
        ordering = self.request.GET.get("sort", "name")
        if ordering not in ["name", "-name", "start_date", "-start_date", "end_date", "-end_date"]:
            ordering = "name"

        return Opportunity.objects.filter(organization=self.request.org).order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opportunity_init_url"] = reverse("opportunity:init", kwargs={"org_slug": self.request.org.slug})

        opportunity_invitations = None
        if self.request.org_membership and self.request.org_membership.is_admin or self.request.user.is_superuser:
            opportunity_invitations = ManagedOpportunityApplication.objects.filter(
                organization=self.request.org, status=ManagedOpportunityApplicationStatus.INVITED
            )

        context["opportunity_invitations"] = opportunity_invitations
        context["base_template"] = "opportunity/base.html"
        return context


class OpportunityCreate(OrganizationUserMemberRoleMixin, CreateView):
    template_name = "opportunity/opportunity_create.html"
    form_class = OpportunityCreationForm

    def get_success_url(self):
        return reverse("opportunity:list", args=(self.request.org.slug,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["domains"] = get_domains_for_user(self.request.user)
        kwargs["user"] = self.request.user
        kwargs["org_slug"] = self.request.org.slug
        return kwargs

    def form_valid(self, form: OpportunityCreationForm) -> HttpResponse:
        response = super().form_valid(form)
        create_learn_modules_and_deliver_units.delay(self.object.id)
        return response


class OpportunityInit(OrganizationUserMemberRoleMixin, CreateView):
    template_name = "opportunity/opportunity_init.html"
    form_class = OpportunityInitForm

    def get_success_url(self):
        return reverse("opportunity:add_payment_units", args=(self.request.org.slug, self.object.id))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["domains"] = get_domains_for_user(self.request.user)
        kwargs["user"] = self.request.user
        kwargs["org_slug"] = self.request.org.slug
        return kwargs

    def form_valid(self, form: OpportunityInitForm) -> HttpResponse:
        response = super().form_valid(form)
        create_learn_modules_and_deliver_units(self.object.id)
        return response


class OpportunityEdit(OrganizationUserMemberRoleMixin, UpdateView):
    model = Opportunity
    template_name = "opportunity/opportunity_edit.html"
    form_class = OpportunityChangeForm

    def get_success_url(self):
        return reverse("opportunity:detail", args=(self.request.org.slug, self.object.id))

    def form_valid(self, form):
        opportunity = form.instance
        opportunity.modified_by = self.request.user.email
        users = form.cleaned_data["users"]
        filter_country = form.cleaned_data["filter_country"]
        filter_credential = form.cleaned_data["filter_credential"]
        if users or filter_country or filter_credential:
            add_connect_users.delay(users, form.instance.id, filter_country, filter_credential)

        additional_users = form.cleaned_data["additional_users"]
        if additional_users:
            for payment_unit in opportunity.paymentunit_set.all():
                opportunity.total_budget += payment_unit.amount * payment_unit.max_total * additional_users
        end_date = form.cleaned_data["end_date"]
        if end_date:
            opportunity.end_date = end_date
        response = super().form_valid(form)
        return response


class OpportunityFinalize(OrganizationUserMemberRoleMixin, UpdateView):
    model = Opportunity
    template_name = "opportunity/opportunity_finalize.html"
    form_class = OpportunityFinalizeForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.paymentunit_set.count() == 0:
            messages.warning(request, "Please configure payment units before setting budget")
            return redirect("opportunity:add_payment_units", org_slug=request.org.slug, pk=self.object.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("opportunity:detail", args=(self.request.org.slug, self.object.id))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        opportunity = self.object
        payment_units = opportunity.paymentunit_set.all()
        budget_per_user = 0
        payment_units_max_total = 0
        for pu in payment_units:
            budget_per_user += pu.amount * pu.max_total
            payment_units_max_total += pu.max_total
        kwargs["budget_per_user"] = budget_per_user
        kwargs["current_start_date"] = opportunity.start_date
        kwargs["opportunity"] = opportunity
        kwargs["payment_units_max_total"] = payment_units_max_total
        return kwargs

    def form_valid(self, form):
        opportunity = form.instance
        opportunity.modified_by = self.request.user.email
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]
        if end_date:
            opportunity.end_date = end_date
        if start_date:
            opportunity.start_date = start_date

        if opportunity.managed:
            ManagedOpportunity.objects.filter(id=opportunity.id).update(
                org_pay_per_visit=form.cleaned_data["org_pay_per_visit"]
            )
        response = super().form_valid(form)
        return response


class OpportunityDetail(OrganizationUserMixin, DetailView):
    model = Opportunity
    template_name = "opportunity/opportunity_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_setup_complete:
            messages.warning(request, "Please complete the opportunity setup to view it")
            return redirect("opportunity:add_payment_units", org_slug=request.org.slug, pk=self.object.id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["export_task_id"] = self.request.GET.get("export_task_id")
        context["visit_export_form"] = VisitExportForm()
        context["export_form"] = PaymentExportForm()
        return context


class OpportunityLearnStatusTableView(OrganizationUserMixin, SingleTableView):
    model = OpportunityAccess
    paginate_by = 25
    table_class = LearnStatusTable
    template_name = "tables/single_table.html"

    def get_queryset(self):
        opportunity_id = self.kwargs["pk"]
        opportunity = get_opportunity_or_404(org_slug=self.request.org.slug, pk=opportunity_id)
        return OpportunityAccess.objects.filter(opportunity=opportunity).order_by("user__name")


class OpportunityPaymentTableView(OrganizationUserMixin, SingleTableView):
    model = OpportunityAccess
    paginate_by = 25
    table_class = OpportunityPaymentTable
    template_name = "tables/single_table.html"

    def get_queryset(self):
        opportunity_id = self.kwargs["pk"]
        opportunity = get_opportunity_or_404(org_slug=self.request.org.slug, pk=opportunity_id)
        return OpportunityAccess.objects.filter(opportunity=opportunity, payment_accrued__gte=0).order_by(
            "-payment_accrued"
        )


class UserPaymentsTableView(OrganizationUserMixin, SingleTableView):
    model = Payment
    paginate_by = 25
    table_class = UserPaymentsTable
    template_name = "opportunity/opportunity_user_payments_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_payment"] = self.object_list.all().first()
        context["access"] = self.access
        context["opportunity"] = self.opportunity
        return context

    def get_queryset(self):
        opportunity_id = self.kwargs["opp_id"]
        self.opportunity = get_opportunity_or_404(org_slug=self.request.org.slug, pk=opportunity_id)
        access_id = self.kwargs["pk"]
        self.access = get_object_or_404(OpportunityAccess, opportunity=self.opportunity, pk=access_id)
        return Payment.objects.filter(opportunity_access=self.access).order_by("-date_paid")


class OpportunityUserLearnProgress(OrganizationUserMixin, DetailView):
    template_name = "opportunity/user_learn_progress.html"

    def get_queryset(self):
        return OpportunityAccess.objects.filter(opportunity_id=self.kwargs.get("opp_id"))


@org_member_required
def export_user_visits(request, **kwargs):
    opportunity_id = kwargs["pk"]
    get_object_or_404(Opportunity, organization=request.org, id=opportunity_id)
    form = VisitExportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect("opportunity:detail", request.org.slug, opportunity_id)

    export_format = form.cleaned_data["format"]
    date_range = DateRanges(form.cleaned_data["date_range"])
    status = form.cleaned_data["status"]
    flatten = form.cleaned_data["flatten_form_data"]

    result = generate_visit_export.delay(opportunity_id, date_range, status, export_format, flatten)
    redirect_url = reverse("opportunity:detail", args=(request.org.slug, opportunity_id))
    return redirect(f"{redirect_url}?export_task_id={result.id}")


@org_member_required
@require_GET
def export_status(request, org_slug, task_id):
    task_meta = AsyncResult(task_id)._get_task_meta()
    status = task_meta.get("status")
    progress = {
        "complete": status == "SUCCESS",
    }
    if status == "FAILURE":
        progress["error"] = task_meta.get("result")
    return render(
        request,
        "opportunity/upload_progress.html",
        {
            "task_id": task_id,
            "current_time": now().microsecond,
            "progress": progress,
        },
    )


@org_member_required
@require_GET
def download_export(request, org_slug, task_id):
    task_meta = AsyncResult(task_id)._get_task_meta()
    saved_filename = task_meta.get("result")
    opportunity_id = task_meta.get("args")[0]
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=opportunity_id)
    op_slug = slugify(opportunity.name)
    export_format = saved_filename.split(".")[-1]
    filename = f"{org_slug}_{op_slug}_export.{export_format}"

    export_file = storages["default"].open(saved_filename)
    return FileResponse(
        export_file, as_attachment=True, filename=filename, content_type=TableExport.FORMATS[export_format]
    )


@org_member_required
@require_POST
def update_visit_status_import(request, org_slug=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=pk)
    file = request.FILES.get("visits")
    try:
        status = bulk_update_visit_status(opportunity, file)
    except ImportException as e:
        messages.error(request, e.message)
    else:
        message = f"Visit status updated successfully for {len(status)} visits."
        if status.missing_visits:
            message += status.get_missing_message()
        messages.success(request, mark_safe(message))
    if opportunity.managed:
        return redirect("opportunity:user_visit_review", org_slug, pk)
    return redirect("opportunity:detail", org_slug, pk)


@org_member_required
def add_budget_existing_users(request, org_slug=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=pk)
    opportunity_access = OpportunityAccess.objects.filter(opportunity=opportunity)
    opportunity_claims = OpportunityClaim.objects.filter(opportunity_access__in=opportunity_access)
    form = AddBudgetExistingUsersForm(opportunity_claims=opportunity_claims)

    if request.method == "POST":
        form = AddBudgetExistingUsersForm(opportunity_claims=opportunity_claims, data=request.POST)
        if form.is_valid():
            selected_users = form.cleaned_data["selected_users"]
            additional_visits = form.cleaned_data["additional_visits"]
            if form.cleaned_data["end_date"]:
                OpportunityClaim.objects.filter(pk__in=selected_users).update(end_date=form.cleaned_data["end_date"])
            if additional_visits:
                OpportunityClaimLimit.objects.filter(opportunity_claim__in=selected_users).update(
                    max_visits=F("max_visits") + additional_visits
                )

            for ocl in OpportunityClaimLimit.objects.filter(opportunity_claim__in=selected_users).all():
                opportunity.total_budget += ocl.payment_unit.amount * additional_visits
            opportunity.save()
            return redirect("opportunity:detail", org_slug, pk)

    return render(
        request,
        "opportunity/add_visits_existing_users.html",
        {
            "form": form,
            "opportunity_claims": opportunity_claims,
            "budget_per_visit": opportunity.budget_per_visit,
            "opportunity": opportunity,
        },
    )


class OpportunityUserStatusTableView(OrganizationUserMixin, SingleTableView):
    model = OpportunityAccess
    paginate_by = 25
    table_class = UserStatusTable
    template_name = "tables/single_table.html"

    def get_queryset(self):
        opportunity_id = self.kwargs["pk"]
        opportunity = get_opportunity_or_404(org_slug=self.request.org.slug, pk=opportunity_id)
        access_objects = get_annotated_opportunity_access(opportunity)
        return access_objects


@org_member_required
def export_users_for_payment(request, **kwargs):
    opportunity_id = kwargs["pk"]
    get_object_or_404(Opportunity, organization=request.org, id=opportunity_id)
    form = PaymentExportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect("opportunity:detail", request.org.slug, opportunity_id)

    export_format = form.cleaned_data["format"]
    result = generate_payment_export.delay(opportunity_id, export_format)
    redirect_url = reverse("opportunity:detail", args=(request.org.slug, opportunity_id))
    return redirect(f"{redirect_url}?export_task_id={result.id}")


@org_member_required
@require_POST
def payment_import(request, org_slug=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=pk)
    file = request.FILES.get("payments")
    try:
        status = bulk_update_payment_status(opportunity, file)
    except ImportException as e:
        messages.error(request, e.message)
    else:
        message = f"Payment status updated successfully for {len(status)} users."
        messages.success(request, mark_safe(message))
    return redirect("opportunity:detail", org_slug, pk)


@org_member_required
def add_payment_units(request, org_slug=None, pk=None):
    if request.POST:
        return add_payment_unit(request, org_slug=request.org, pk=pk)
    opportunity = get_opportunity_or_404(org_slug=request.org.slug, pk=pk)
    return render(request, "opportunity/add_payment_units.html", dict(opportunity=opportunity))


@org_member_required
def add_payment_unit(request, org_slug=None, pk=None):
    opportunity = get_opportunity_or_404(org_slug=request.org.slug, pk=pk)
    deliver_units = DeliverUnit.objects.filter(
        Q(payment_unit__isnull=True) | Q(payment_unit__opportunity__active=False), app=opportunity.deliver_app
    )
    form = PaymentUnitForm(
        deliver_units=deliver_units,
        data=request.POST or None,
        payment_units=opportunity.paymentunit_set.filter(parent_payment_unit__isnull=True).all(),
    )
    if form.is_valid():
        form.instance.opportunity = opportunity
        form.save()
        required_deliver_units = form.cleaned_data["required_deliver_units"]
        DeliverUnit.objects.filter(id__in=required_deliver_units, payment_unit__isnull=True).update(
            payment_unit=form.instance.id
        )
        optional_deliver_units = form.cleaned_data["optional_deliver_units"]
        DeliverUnit.objects.filter(id__in=optional_deliver_units, payment_unit__isnull=True).update(
            payment_unit=form.instance.id, optional=True
        )
        sub_payment_units = form.cleaned_data["payment_units"]
        PaymentUnit.objects.filter(id__in=sub_payment_units, parent_payment_unit__isnull=True).update(
            parent_payment_unit=form.instance.id
        )
        messages.success(request, f"Payment unit {form.instance.name} created.")
        return redirect("opportunity:add_payment_units", org_slug=request.org.slug, pk=opportunity.id)
    elif request.POST:
        messages.error(request, "Invalid Data")
        return redirect("opportunity:add_payment_units", org_slug=request.org.slug, pk=opportunity.id)
    return render(
        request,
        "partial_form.html" if request.GET.get("partial") == "True" else "form.html",
        dict(title=f"{request.org.slug} - {opportunity.name}", form_title="Payment Unit Create", form=form),
    )


@org_member_required
def edit_payment_unit(request, org_slug=None, opp_id=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=opp_id)
    payment_unit = get_object_or_404(PaymentUnit, id=pk, opportunity=opportunity)
    deliver_units = DeliverUnit.objects.filter(
        Q(payment_unit__isnull=True) | Q(payment_unit=payment_unit) | Q(payment_unit__opportunity__active=False),
        app=opportunity.deliver_app,
    )
    exclude_payment_units = [payment_unit.pk]
    if payment_unit.parent_payment_unit_id:
        exclude_payment_units.append(payment_unit.parent_payment_unit_id)
    payment_unit_deliver_units = {deliver_unit.pk for deliver_unit in payment_unit.deliver_units.all()}
    opportunity_payment_units = (
        opportunity.paymentunit_set.filter(
            Q(parent_payment_unit=payment_unit.pk) | Q(parent_payment_unit__isnull=True)
        )
        .exclude(pk__in=exclude_payment_units)
        .all()
    )
    form = PaymentUnitForm(
        deliver_units=deliver_units,
        instance=payment_unit,
        data=request.POST or None,
        payment_units=opportunity_payment_units,
    )
    if form.is_valid():
        form.save()
        required_deliver_units = form.cleaned_data["required_deliver_units"]
        DeliverUnit.objects.filter(id__in=required_deliver_units).update(payment_unit=form.instance.id, optional=False)
        optional_deliver_units = form.cleaned_data["optional_deliver_units"]
        DeliverUnit.objects.filter(id__in=optional_deliver_units).update(payment_unit=form.instance.id, optional=True)
        sub_payment_units = form.cleaned_data["payment_units"]
        PaymentUnit.objects.filter(id__in=sub_payment_units, parent_payment_unit__isnull=True).update(
            parent_payment_unit=form.instance.id
        )
        # Remove deliver units which are not selected anymore
        deliver_units = required_deliver_units + optional_deliver_units
        removed_deliver_units = payment_unit_deliver_units - {int(deliver_unit) for deliver_unit in deliver_units}
        DeliverUnit.objects.filter(id__in=removed_deliver_units).update(payment_unit=None, optional=False)
        removed_payment_units = {payment_unit.id for payment_unit in opportunity_payment_units} - {
            int(payment_unit_id) for payment_unit_id in sub_payment_units
        }
        PaymentUnit.objects.filter(id__in=removed_payment_units, parent_payment_unit=form.instance.id).update(
            parent_payment_unit=None
        )
        messages.success(request, f"Payment unit {form.instance.name} updated. Please reset the budget")
        return redirect("opportunity:finalize", org_slug=request.org.slug, pk=opportunity.id)
    return render(
        request,
        "form.html",
        dict(title=f"{request.org.slug} - {opportunity.name}", form_title="Payment Unit Edit", form=form),
    )


class OpportunityPaymentUnitTableView(OrganizationUserMixin, SingleTableView):
    model = PaymentUnit
    paginate_by = 25
    table_class = PaymentUnitTable
    template_name = "tables/single_table.html"

    def get_queryset(self):
        opportunity_id = self.kwargs["pk"]
        opportunity = get_opportunity_or_404(org_slug=self.request.org.slug, pk=opportunity_id)
        return PaymentUnit.objects.filter(opportunity=opportunity).order_by("name")


@org_member_required
def export_user_status(request, **kwargs):
    opportunity_id = kwargs["pk"]
    get_opportunity_or_404(org_slug=request.org.slug, pk=opportunity_id)
    form = PaymentExportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect("opportunity:detail", request.org.slug, opportunity_id)

    export_format = form.cleaned_data["format"]
    result = generate_user_status_export.delay(opportunity_id, export_format)
    redirect_url = reverse("opportunity:detail", args=(request.org.slug, opportunity_id))
    return redirect(f"{redirect_url}?export_task_id={result.id}")


class OpportunityDeliverStatusTable(OrganizationUserMixin, SingleTableView):
    model = OpportunityAccess
    paginate_by = 25
    table_class = DeliverStatusTable
    template_name = "tables/single_table.html"

    def get_queryset(self):
        opportunity_id = self.kwargs["pk"]
        opportunity = get_opportunity_or_404(pk=opportunity_id, org_slug=self.request.org.slug)
        access_objects = get_annotated_opportunity_access_deliver_status(opportunity)
        return access_objects


@org_member_required
def export_deliver_status(request, **kwargs):
    opportunity_id = kwargs["pk"]
    get_opportunity_or_404(pk=opportunity_id, org_slug=request.org.slug)
    form = PaymentExportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect("opportunity:detail", request.org.slug, opportunity_id)

    export_format = form.cleaned_data["format"]
    result = generate_deliver_status_export.delay(opportunity_id, export_format)
    redirect_url = reverse("opportunity:detail", args=(request.org.slug, opportunity_id))
    return redirect(f"{redirect_url}?export_task_id={result.id}")


@org_viewer_required
def user_visits_list(request, org_slug=None, opp_id=None, pk=None):
    opportunity = get_opportunity_or_404(pk=opp_id, org_slug=request.org.slug)
    opportunity_access = get_object_or_404(OpportunityAccess, pk=pk, opportunity=opportunity)
    user_visits = opportunity_access.uservisit_set.order_by("visit_date")
    user_visits_table = UserVisitTable(user_visits)
    return render(
        request,
        "opportunity/user_visits_list.html",
        context=dict(opportunity=opportunity, table=user_visits_table, user_name=opportunity_access.display_name),
    )


@org_member_required
@require_POST
def payment_delete(request, org_slug=None, opp_id=None, access_id=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, pk=opp_id)
    opportunity_access = get_object_or_404(OpportunityAccess, pk=access_id, opportunity=opportunity)
    payment = get_object_or_404(Payment, opportunity_access=opportunity_access, pk=pk)
    payment.delete()
    return redirect("opportunity:user_payments_table", org_slug=org_slug, opp_id=opp_id, pk=access_id)


@org_viewer_required
def user_profile(request, org_slug=None, opp_id=None, pk=None):
    access = get_object_or_404(OpportunityAccess, pk=pk, accepted=True)
    user_visits = UserVisit.objects.filter(opportunity_access=access)
    user_catchments = CatchmentArea.objects.filter(opportunity_access=access)
    user_visit_data = []
    for user_visit in user_visits:
        if not user_visit.location:
            continue
        lat, lng, elevation, precision = list(map(float, user_visit.location.split(" ")))
        user_visit_data.append(
            dict(
                entity_name=user_visit.entity_name,
                visit_date=user_visit.visit_date.date(),
                lat=lat,
                lng=lng,
                precision=precision,
            )
        )
    # user for centering the User visits map
    lat_avg = 0.0
    lng_avg = 0.0
    if user_visit_data:
        lat_avg = reduce(lambda x, y: x + float(y["lat"]), user_visit_data, 0.0) / len(user_visit_data)
        lng_avg = reduce(lambda x, y: x + float(y["lng"]), user_visit_data, 0.0) / len(user_visit_data)

    pending_completed_work_count = len(
        [
            cw
            for cw in CompletedWork.objects.filter(opportunity_access=access, status=CompletedWorkStatus.pending)
            if cw.approved_count
        ]
    )
    user_catchment_data = [
        {
            "name": catchment.name,
            "lat": float(catchment.latitude),
            "lng": float(catchment.longitude),
            "radius": catchment.radius,
            "active": catchment.active,
        }
        for catchment in user_catchments
    ]
    pending_payment = max(access.payment_accrued - access.total_paid, 0)
    return render(
        request,
        "opportunity/user_profile.html",
        context=dict(
            access=access,
            user_visits=user_visit_data,
            lat_avg=lat_avg,
            lng_avg=lng_avg,
            MAPBOX_TOKEN=settings.MAPBOX_TOKEN,
            pending_completed_work_count=pending_completed_work_count,
            pending_payment=pending_payment,
            user_catchments=user_catchment_data,
        ),
    )


@org_admin_required
def send_message_mobile_users(request, org_slug=None, pk=None):
    opportunity = get_opportunity_or_404(pk=pk, org_slug=request.org.slug)
    user_ids = OpportunityAccess.objects.filter(opportunity=opportunity, accepted=True).values_list(
        "user_id", flat=True
    )
    users = User.objects.filter(pk__in=user_ids)
    form = SendMessageMobileUsersForm(users=users, data=request.POST or None)

    if form.is_valid():
        selected_user_ids = form.cleaned_data["selected_users"]
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]
        message_type = form.cleaned_data["message_type"]
        if "notification" in message_type:
            send_push_notification_task.delay(selected_user_ids, title, body)
        if "sms" in message_type:
            send_sms_task.delay(selected_user_ids, body)
        return redirect("opportunity:detail", org_slug=request.org.slug, pk=pk)

    return render(
        request,
        "opportunity/send_message.html",
        context=dict(
            title=f"{request.org.slug} - {opportunity.name}",
            form_title="Send Message",
            form=form,
            users=users,
            user_ids=list(user_ids),
        ),
    )


# used for loading learn_app and deliver_app dropdowns
@org_member_required
def get_application(request, org_slug=None):
    domain = request.GET.get("learn_app_domain") or request.GET.get("deliver_app_domain")
    applications = get_applications_for_user_by_domain(request.user, domain)
    active_opps = Opportunity.objects.filter(
        Q(learn_app__cc_domain=domain) | Q(deliver_app__cc_domain=domain),
        active=True,
        end_date__lt=datetime.date.today(),
    ).select_related("learn_app", "deliver_app")
    existing_apps = set()
    for opp in active_opps:
        if opp.learn_app.cc_domain == domain:
            existing_apps.add(opp.learn_app.cc_app_id)
        if opp.deliver_app.cc_domain == domain:
            existing_apps.add(opp.deliver_app.cc_app_id)
    options = []
    for app in applications:
        if app["id"] not in existing_apps:
            value = json.dumps(app)
            name = app["name"]
            options.append(format_html("<option value='{}'>{}</option>", value, name))
    return HttpResponse("\n".join(options))


@org_viewer_required
def visit_verification(request, org_slug=None, pk=None):
    user_visit = get_object_or_404(UserVisit, pk=pk)
    serializer = XFormSerializer(data=user_visit.form_json)
    access_id = OpportunityAccess.objects.get(user=user_visit.user, opportunity=user_visit.opportunity).id
    serializer.is_valid()
    xform = serializer.save()
    user_forms = []
    other_forms = []
    lat = None
    lon = None
    precision = None
    if user_visit.location:
        locations = UserVisit.objects.filter(opportunity=user_visit.opportunity).exclude(pk=pk).select_related("user")
        lat, lon, _, precision = user_visit.location.split(" ")
        for loc in locations:
            if loc.location is None:
                continue
            other_lat, other_lon, _, other_precision = loc.location.split(" ")
            dist = distance.distance((lat, lon), (other_lat, other_lon))
            if dist.m <= 250:
                if user_visit.user_id == loc.user_id:
                    user_forms.append((loc, dist.m, other_lat, other_lon, other_precision))
                else:
                    other_forms.append((loc, dist.m, other_lat, other_lon, other_precision))
        user_forms.sort(key=lambda x: x[1])
        other_forms.sort(key=lambda x: x[1])
    reason = user_visit.reason
    if user_visit.flag_reason and not reason:
        reason = "\n".join([flag[1] for flag in user_visit.flag_reason.get("flags", [])])
    return render(
        request,
        "opportunity/visit_verification.html",
        context={
            "visit": user_visit,
            "xform": xform,
            "access_id": access_id,
            "user_forms": user_forms[:5],
            "other_forms": other_forms[:5],
            "visit_lat": lat,
            "visit_lon": lon,
            "visit_precision": precision,
            "MAPBOX_TOKEN": settings.MAPBOX_TOKEN,
            "reason": reason,
        },
    )


@org_member_required
def approve_visit(request, org_slug=None, pk=None):
    user_visit = UserVisit.objects.get(pk=pk)
    user_visit.status = VisitValidationStatus.approved
    if user_visit.opportunity.managed:
        user_visit.review_created_on = now()
    user_visit.save()
    opp_id = user_visit.opportunity_id
    access = OpportunityAccess.objects.get(user_id=user_visit.user_id, opportunity_id=opp_id)
    update_payment_accrued(opportunity=access.opportunity, users=[access.user])
    if user_visit.opportunity.managed:
        return redirect("opportunity:user_visit_review", org_slug, pk)
    return redirect("opportunity:user_visits_list", org_slug=org_slug, opp_id=user_visit.opportunity.id, pk=access.id)


@org_member_required
@require_POST
def reject_visit(request, org_slug=None, pk=None):
    user_visit = UserVisit.objects.get(pk=pk)
    reason = request.POST.get("reason")
    user_visit.status = VisitValidationStatus.rejected
    user_visit.reason = reason
    if user_visit.opportunity.managed:
        user_visit.review_created_on = now()
    user_visit.save()
    access = OpportunityAccess.objects.get(user_id=user_visit.user_id, opportunity_id=user_visit.opportunity_id)
    update_payment_accrued(opportunity=access.opportunity, users=[access.user])
    if user_visit.opportunity.managed:
        return redirect("opportunity:user_visit_review", org_slug, pk)
    return redirect("opportunity:user_visits_list", org_slug=org_slug, opp_id=user_visit.opportunity_id, pk=access.id)


@org_member_required
def fetch_attachment(self, org_slug, blob_id):
    blob_meta = BlobMeta.objects.get(blob_id=blob_id)
    attachment = storages["default"].open(blob_id)
    return FileResponse(attachment, filename=blob_meta.name, content_type=blob_meta.content_type)


@org_member_required
def verification_flags_config(request, org_slug=None, pk=None):
    opportunity = get_opportunity_or_404(pk=pk, org_slug=request.org.slug)
    verification_flags = OpportunityVerificationFlags.objects.filter(opportunity=opportunity).first()
    form = OpportunityVerificationFlagsConfigForm(instance=verification_flags, data=request.POST or None)

    if form.is_valid():
        verification_flags = form.save(commit=False)
        verification_flags.opportunity = opportunity
        verification_flags.save()
        return redirect("opportunity:detail", request.org.slug, opportunity.id)

    return render(
        request,
        "form.html",
        context=dict(
            title=f"{request.org.slug} - {opportunity.name}", form_title="Verification Flags Configuration", form=form
        ),
    )


class OpportunityCompletedWorkTable(OrganizationUserMixin, SingleTableView):
    model = CompletedWork
    paginate_by = 25
    table_class = CompletedWorkTable
    template_name = "tables/single_table.html"

    def get_queryset(self):
        opportunity_id = self.kwargs["pk"]
        opportunity = get_object_or_404(Opportunity, organization=self.request.org, id=opportunity_id)
        access_objects = OpportunityAccess.objects.filter(opportunity=opportunity)
        return list(
            filter(lambda cw: cw.completed, CompletedWork.objects.filter(opportunity_access__in=access_objects))
        )


@org_member_required
def export_completed_work(request, **kwargs):
    opportunity_id = kwargs["pk"]
    get_object_or_404(Opportunity, organization=request.org, id=opportunity_id)
    form = PaymentExportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect("opportunity:detail", request.org.slug, opportunity_id)

    export_format = form.cleaned_data["format"]
    result = generate_work_status_export.delay(opportunity_id, export_format)
    redirect_url = reverse("opportunity:detail", args=(request.org.slug, opportunity_id))
    return redirect(f"{redirect_url}?export_task_id={result.id}")


@org_member_required
@require_POST
def update_completed_work_status_import(request, org_slug=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=pk)
    file = request.FILES.get("visits")
    try:
        status = bulk_update_completed_work_status(opportunity, file)
    except ImportException as e:
        messages.error(request, e.message)
    else:
        message = f"Payment Verification status updated successfully for {len(status)} completed works."
        if status.missing_completed_works:
            message += status.get_missing_message()
        messages.success(request, mark_safe(message))
    return redirect("opportunity:detail", org_slug, pk)


@org_member_required
@require_POST
def suspend_user(request, org_slug=None, opp_id=None, pk=None):
    access = get_object_or_404(OpportunityAccess, opportunity_id=opp_id, id=pk)
    access.suspended = True
    access.suspension_date = now()
    access.suspension_reason = request.POST.get("reason", "")
    access.save()

    # Clear the cached opportunity access for the suspended user
    remove_opportunity_access_cache(access.user, access.opportunity)

    return redirect("opportunity:user_profile", org_slug, opp_id, pk)


@org_member_required
def revoke_user_suspension(request, org_slug=None, opp_id=None, pk=None):
    access = get_object_or_404(OpportunityAccess, opportunity_id=opp_id, id=pk)
    access.suspended = False
    access.save()
    remove_opportunity_access_cache(access.user, access.opportunity)
    next = request.GET.get("next", "/")
    return redirect(next)


@org_member_required
def suspended_users_list(request, org_slug=None, pk=None):
    opportunity = get_object_or_404(Opportunity, organization=request.org, id=pk)
    access_objects = OpportunityAccess.objects.filter(opportunity=opportunity, suspended=True)
    table = SuspendedUsersTable(access_objects)
    return render(request, "opportunity/suspended_users.html", dict(table=table, opportunity=opportunity))


@org_member_required
def export_catchment_area(request, **kwargs):
    opportunity_id = kwargs["pk"]
    get_opportunity_or_404(pk=opportunity_id, org_slug=request.org.slug)
    form = PaymentExportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect("opportunity:detail", request.org.slug, opportunity_id)

    export_format = form.cleaned_data["format"]
    result = generate_catchment_area_export.delay(opportunity_id, export_format)
    redirect_url = reverse("opportunity:detail", args=(request.org.slug, opportunity_id))
    return redirect(f"{redirect_url}?export_task_id={result.id}")


@org_member_required
@require_POST
def import_catchment_area(request, org_slug=None, pk=None):
    opportunity = get_opportunity_or_404(pk=pk, org_slug=request.org.slug)
    file = request.FILES.get("catchments")
    try:
        status = bulk_update_catchments(opportunity, file)
    except ImportException as e:
        messages.error(request, e.message)
    else:
        message = f"{len(status)} catchment areas were updated successfully and {status.new_catchments} were created."
        messages.success(request, mark_safe(message))
    return redirect("opportunity:detail", org_slug, pk)


@org_admin_required
@require_POST
def apply_opportunity_invite(request, application_id, org_slug=None, pk=None):
    application = get_object_or_404(
        ManagedOpportunityApplication, id=application_id, status=ManagedOpportunityApplicationStatus.INVITED
    )
    application.status = ManagedOpportunityApplicationStatus.APPLIED
    application.modified_by = request.user.email
    application.save()
    messages.success(
        request,
        f"Application for the opportunity '{application.managed_opportunity.name}' has been successfully submitted.",
    )
    return redirect("opportunity:list", org_slug)


@org_member_required
def user_visit_review(request, org_slug, opp_id):
    opportunity = get_opportunity_or_404(opp_id, org_slug)
    if not opportunity.managed:
        return redirect("opportunity:detail", org_slug, opp_id)
    is_program_manager = request.org_membership.is_admin and request.org.program_manager
    user_visit_reviews = UserVisit.objects.filter(opportunity=opportunity, review_created_on__isnull=False).order_by(
        "visit_date"
    )
    table = UserVisitReviewTable(user_visit_reviews)
    if not is_program_manager:
        table.exclude = ("pk",)
    if request.POST and is_program_manager:
        review_status = request.POST.get("review_status")
        updated_reviews = request.POST.getlist("pk")
        if review_status in ["approved", "rejected"]:
            UserVisit.objects.filter(pk__in=updated_reviews).update(review_status=review_status)

    return render(
        request,
        "opportunity/user_visit_review.html",
        context=dict(table=table, user_visit_ids=[v.pk for v in user_visit_reviews]),
    )


@org_member_required
def payment_report(request, org_slug, pk):
    opportunity = get_opportunity_or_404(pk, org_slug)
    if not opportunity.managed:
        return redirect("opportunity:detail", org_slug, pk)
    payment_units = PaymentUnit.objects.filter(opportunity=opportunity)
    PaymentReportData = namedtuple(
        "PaymentReportData", ["payment_unit", "approved", "user_payment_accrued", "nm_payment_accrued"]
    )
    data = []
    total_paid_users = sum(Payment.objects.filter(opportunity_access__opportunity=opportunity).values_list("amount"))
    total_user_payment_accrued = 0
    for payment_unit in payment_units:
        completed_works = CompletedWork.objects.filter(
            opportunity_access__opportunity=opportunity, status=CompletedWorkStatus.approved
        )
        completed_work_count = len(completed_works)
        user_payment_accrued = sum([cw.payment_accrued for cw in completed_works])
        total_user_payment_accrued += user_payment_accrued
        data.append(
            PaymentReportData(
                payment_unit.name,
                completed_work_count,
                user_payment_accrued,
                completed_work_count * opportunity.managedopportunity.org_pay_per_visit,
            )
        )
    table = PaymentReportTable(data)
    return render(
        request,
        "opportunity/payment_report.html",
        context=dict(
            table=table,
            opportunity=opportunity,
            total_paid_users=total_paid_users,
            total_user_payment_accrued=total_user_payment_accrued,
        ),
    )
