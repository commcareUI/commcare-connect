from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Field, Row, Submit
from dateutil.relativedelta import relativedelta
from django import forms
from django.db.models import TextChoices
from django.utils.timezone import now

from commcare_connect.opportunity.models import (
    CommCareApp,
    HQApiKey,
    Opportunity,
    OpportunityAccess,
    PaymentUnit,
    VisitValidationStatus,
)
from commcare_connect.organization.models import Organization
from commcare_connect.users.models import User


class OpportunityChangeForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            "name",
            "description",
            "active",
            "currency",
            "short_description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Field("name")),
            Row(Field("active")),
            Row(Field("description")),
            Row(Field("short_description")),
            Row(Field("currency")),
            Row(
                Field("additional_users", wrapper_class="form-group col-md-6 mb-0"),
                Field("end_date", wrapper_class="form-group col-md-6 mb-0"),
            ),
            HTML("<hr />"),
            Row(Field("users")),
            Submit("submit", "Submit"),
        )

        self.fields["users"] = forms.CharField(
            widget=forms.Textarea,
            help_text="Enter the phone numbers of the users you want to add to this opportunity, one on each line.",
            required=False,
        )
        self.fields["additional_users"] = forms.IntegerField(
            required=False, help_text="Adds budget for additional users."
        )
        self.fields["end_date"] = forms.DateField(
            widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            required=False,
            help_text="Extends opportunity end date for all users.",
        )

    def clean_users(self):
        user_data = self.cleaned_data["users"]
        split_users = [line.strip() for line in user_data.splitlines() if line.strip()]
        return split_users


class OpportunityCreationForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            "name",
            "description",
            "short_description",
            "end_date",
            "max_visits_per_user",
            "daily_max_visits_per_user",
            "budget_per_visit",
            "total_budget",
            "currency",
        ]
        widgets = {
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.applications = kwargs.pop("applications", [])
        self.user = kwargs.pop("user", {})
        self.org_slug = kwargs.pop("org_slug", "")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Field("name")),
            Row(Field("description")),
            Row(Field("short_description")),
            Row(Field("end_date")),
            Row(
                Field("max_visits_per_user", wrapper_class="form-group col-md-4 mb-0", x_model="maxVisits"),
                Field("daily_max_visits_per_user", wrapper_class="form-group col-md-4 mb-0"),
                Field("budget_per_visit", wrapper_class="form-group col-md-4 mb-0", x_model="visitBudget"),
            ),
            Row(
                Field("max_users", wrapper_class="form-group col-md-4 mb-0", x_model="maxUsers"),
                Field(
                    "total_budget",
                    wrapper_class="form-group col-md-4 mb-0",
                    readonly=True,
                    x_model="totalBudget()",
                ),
                Field("currency", wrapper_class="form-group col-md-4 mb-0"),
            ),
            Row(Field("learn_app")),
            Row(Field("learn_app_description")),
            Row(Field("learn_app_passing_score")),
            Row(Field("deliver_app")),
            Row(Field("api_key")),
            Submit("submit", "Submit"),
        )

        app_choices = [(app["id"], app["name"]) for app in self.applications]

        self.fields["learn_app"] = forms.ChoiceField(choices=app_choices)
        self.fields["learn_app_description"] = forms.CharField(widget=forms.Textarea)
        self.fields["learn_app_passing_score"] = forms.IntegerField(max_value=100, min_value=0)
        self.fields["deliver_app"] = forms.ChoiceField(choices=app_choices)
        self.fields["deliver_app"].widget.attrs.update({"id": "deliver_app_select"})
        self.fields["api_key"] = forms.CharField(max_length=50)
        self.fields["total_budget"].widget.attrs.update({"class": "form-control-plaintext"})
        self.fields["max_users"] = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            if cleaned_data["learn_app"] == cleaned_data["deliver_app"]:
                self.add_error("learn_app", "Learn app and Deliver app cannot be same")
                self.add_error("deliver_app", "Learn app and Deliver app cannot be same")

            if cleaned_data["daily_max_visits_per_user"] > cleaned_data["max_visits_per_user"]:
                self.add_error(
                    "daily_max_visits_per_user",
                    "Daily max visits per user cannot be greater than Max visits per user",
                )

            if cleaned_data["budget_per_visit"] > cleaned_data["total_budget"]:
                self.add_error("budget_per_visit", "Budget per visit cannot be greater than Total budget")

            if cleaned_data["end_date"] < now().date():
                self.add_error("end_date", "Please enter the correct end date for this opportunity")

    def save(self, commit=True):
        organization = Organization.objects.filter(slug=self.org_slug).first()

        for app in self.applications:
            if app["id"] == self.cleaned_data["learn_app"]:
                self.instance.learn_app, _ = CommCareApp.objects.get_or_create(
                    cc_app_id=app["id"],
                    cc_domain=app["domain"],
                    organization=organization,
                    defaults={
                        "name": app["name"],
                        "created_by": self.user.email,
                        "modified_by": self.user.email,
                        "description": self.cleaned_data["learn_app_description"],
                        "passing_score": self.cleaned_data["learn_app_passing_score"],
                    },
                )

            if app["id"] == self.cleaned_data["deliver_app"]:
                self.instance.deliver_app, _ = CommCareApp.objects.get_or_create(
                    cc_app_id=app["id"],
                    cc_domain=app["domain"],
                    organization=organization,
                    defaults={
                        "name": app["name"],
                        "created_by": self.user.email,
                        "modified_by": self.user.email,
                    },
                )

        self.instance.created_by = self.user.email
        self.instance.modified_by = self.user.email
        self.instance.organization = organization

        api_key, _ = HQApiKey.objects.get_or_create(user=self.user, api_key=self.cleaned_data["api_key"])
        self.instance.api_key = api_key
        super().save(commit=commit)

        return self.instance


class DateRanges(TextChoices):
    LAST_7_DAYS = "last_7_days", "Last 7 days"
    LAST_30_DAYS = "last_30_days", "Last 30 days"
    LAST_90_DAYS = "last_90_days", "Last 90 days"
    LAST_YEAR = "last_year", "Last year"
    ALL = "all", "All"

    def get_cutoff_date(self):
        match self:
            case DateRanges.LAST_7_DAYS:
                return now() - relativedelta(days=7)
            case DateRanges.LAST_30_DAYS:
                return now() - relativedelta(days=30)
            case DateRanges.LAST_90_DAYS:
                return now() - relativedelta(days=90)
            case DateRanges.LAST_YEAR:
                return now() - relativedelta(years=1)
            case DateRanges.ALL:
                return None


class VisitExportForm(forms.Form):
    format = forms.ChoiceField(choices=(("csv", "CSV"), ("xlsx", "Excel")), initial="xlsx")
    date_range = forms.ChoiceField(choices=DateRanges.choices, initial=DateRanges.LAST_30_DAYS)
    status = forms.MultipleChoiceField(choices=[("all", "All")] + VisitValidationStatus.choices, initial=["all"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Field("format")),
            Row(Field("date_range")),
            Row(Field("status")),
        )
        self.helper.form_tag = False

    def clean_status(self):
        statuses = self.cleaned_data["status"]
        if not statuses or "all" in statuses:
            return []

        return [VisitValidationStatus(status) for status in statuses]


class PaymentExportForm(forms.Form):
    format = forms.ChoiceField(choices=(("csv", "CSV"), ("xlsx", "Excel")), initial="xlsx")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Field("format")),
        )
        self.helper.form_tag = False


class OpportunityAccessCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(username__isnull=False))

    class Meta:
        model = OpportunityAccess
        fields = "__all__"


class AddBudgetExistingUsersForm(forms.Form):
    additional_visits = forms.IntegerField(
        widget=forms.NumberInput(attrs={"x-model": "additionalVisits"}), required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-input", "x-model": "end_date"}),
        label="Extended Opportunity End date",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        opportunity_claims = kwargs.pop("opportunity_claims", [])
        super().__init__(*args, **kwargs)

        choices = [(opp_claim.id, opp_claim.id) for opp_claim in opportunity_claims]
        self.fields["selected_users"] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)


class PaymentUnitForm(forms.ModelForm):
    class Meta:
        model = PaymentUnit
        fields = ["name", "description", "amount"]

    def __init__(self, *args, **kwargs):
        deliver_units = kwargs.pop("deliver_units", [])
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Field("name")),
            Row(Field("description")),
            Row(Field("amount")),
            Row(Field("deliver_units")),
            Submit(name="submit", value="Submit"),
        )

        choices = [(deliver_unit.id, deliver_unit.name) for deliver_unit in deliver_units]
        self.fields["deliver_units"] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
        if PaymentUnit.objects.filter(pk=self.instance.pk).exists():
            self.fields["deliver_units"].initial = [
                deliver_unit.pk for deliver_unit in self.instance.deliver_units.all()
            ]
