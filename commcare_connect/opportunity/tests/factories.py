from datetime import timezone

from factory import DictFactory, Faker, LazyAttribute, SelfAttribute, SubFactory
from factory.django import DjangoModelFactory

from commcare_connect.opportunity.models import VisitValidationStatus
from commcare_connect.users.tests.factories import OrganizationFactory


class ApplicationFactory(DictFactory):
    id = Faker("pystr")
    name = Faker("name")
    domain = Faker("name")


class CommCareAppFactory(DjangoModelFactory):
    organization = SubFactory(OrganizationFactory)
    cc_domain = Faker("name")
    cc_app_id = Faker("uuid4")
    name = Faker("name")
    description = Faker("text")
    passing_score = Faker("pyint", min_value=50, max_value=100, step=5)

    class Meta:
        model = "opportunity.CommCareApp"


class HQApiKeyFactory(DjangoModelFactory):
    api_key = Faker("uuid4")
    user = SubFactory("commcare_connect.users.tests.factories.UserFactory")

    class Meta:
        model = "opportunity.HQApiKey"


class OpportunityFactory(DjangoModelFactory):
    organization = SubFactory(OrganizationFactory)
    name = Faker("name")
    description = Faker("text")
    short_description = Faker("pystr", max_chars=50)
    active = True
    learn_app = SubFactory(CommCareAppFactory, organization=SelfAttribute("..organization"))
    deliver_app = SubFactory(CommCareAppFactory, organization=SelfAttribute("..organization"))
    end_date = Faker("future_date")
    # to be removed
    budget_per_visit = Faker("pyint", min_value=1, max_value=10)
    total_budget = Faker("pyint", min_value=1000, max_value=10000)
    api_key = SubFactory(HQApiKeyFactory)

    class Meta:
        model = "opportunity.Opportunity"


class LearnModuleFactory(DjangoModelFactory):
    app = SubFactory(CommCareAppFactory)
    slug = Faker("pystr")
    name = Faker("name")
    description = Faker("text")
    time_estimate = Faker("pyint", min_value=1, max_value=10)

    class Meta:
        model = "opportunity.LearnModule"


class PaymentUnitFactory(DjangoModelFactory):
    opportunity = SubFactory(OpportunityFactory)
    name = Faker("name")
    description = Faker("text")
    amount = Faker("pyint", min_value=1, max_value=10)
    max_daily = Faker("pyint", min_value=1, max_value=10)
    max_total = LazyAttribute(lambda o: o.max_daily * 2)

    # parent_payment_unit = SubFactory("commcare_connect.opportunity.tests.factories.PaymentUnitFactory")

    class Meta:
        model = "opportunity.PaymentUnit"


class DeliverUnitFactory(DjangoModelFactory):
    app = SubFactory(CommCareAppFactory)
    slug = Faker("pystr")
    name = Faker("name")
    payment_unit = SubFactory(PaymentUnitFactory)

    class Meta:
        model = "opportunity.DeliverUnit"


class OpportunityAccessFactory(DjangoModelFactory):
    opportunity = SubFactory(OpportunityFactory)
    user = SubFactory("commcare_connect.users.tests.factories.MobileUserFactory")

    class Meta:
        model = "opportunity.OpportunityAccess"


class CompletedWorkFactory(DjangoModelFactory):
    opportunity_access = SubFactory(OpportunityAccessFactory)
    payment_unit = SubFactory(PaymentUnitFactory)
    entity_id = Faker("uuid4")
    entity_name = Faker("name")

    class Meta:
        model = "opportunity.CompletedWork"


class UserVisitFactory(DjangoModelFactory):
    opportunity = SubFactory(OpportunityFactory)
    user = SubFactory("commcare_connect.users.tests.factories.UserFactory")
    deliver_unit = SubFactory(DeliverUnitFactory)
    status = Faker("enum", enum_cls=VisitValidationStatus)
    visit_date = Faker("date_time", tzinfo=timezone.utc)
    form_json = Faker("pydict", value_types=[str, int, float, bool])
    xform_id = Faker("uuid4")

    class Meta:
        model = "opportunity.UserVisit"


class OpportunityClaimFactory(DjangoModelFactory):
    opportunity_access = SubFactory(OpportunityAccessFactory)
    end_date = Faker("date")
    date_claimed = Faker("date")

    class Meta:
        model = "opportunity.OpportunityClaim"


class OpportunityClaimLimitFactory(DjangoModelFactory):
    opportunity_claim = SubFactory(OpportunityClaimFactory)
    payment_unit = SubFactory(PaymentUnitFactory)
    max_visits = Faker("pyint", min_value=1, max_value=100)

    class Meta:
        model = "opportunity.OpportunityClaimLimit"


class CompletedModuleFactory(DjangoModelFactory):
    opportunity = SubFactory(OpportunityFactory)
    user = SubFactory("commcare_connect.users.tests.factories.UserFactory")
    date = Faker("date_time", tzinfo=timezone.utc)
    module = SubFactory(LearnModuleFactory, app=SelfAttribute("..opportunity.learn_app"))
    duration = Faker("time_delta")

    class Meta:
        model = "opportunity.CompletedModule"


class AssessmentFactory(DjangoModelFactory):
    opportunity = SubFactory(OpportunityFactory)
    user = SubFactory("commcare_connect.users.tests.factories.UserFactory")
    app = SubFactory(CommCareAppFactory)
    passed = True
    score = Faker("pyint", min_value=75, max_value=100)
    passing_score = Faker("pyint", min_value=1, max_value=50)
    date = Faker("date_time", tzinfo=timezone.utc)

    class Meta:
        model = "opportunity.Assessment"


class UserInviteFactory(DjangoModelFactory):
    opportunity = SubFactory(OpportunityFactory)
    phone_number = Faker("word")
    message_sid = Faker("word")
    opportunity_access = SubFactory(OpportunityAccessFactory)

    class Meta:
        model = "opportunity.UserInvite"
