import pytest
from django.utils.timezone import now
from tablib import Dataset

from commcare_connect.opportunity.export import export_user_status_table, export_user_visit_data, get_flattened_dataset
from commcare_connect.opportunity.forms import DateRanges
from commcare_connect.opportunity.models import Opportunity, UserVisit
from commcare_connect.opportunity.tests.factories import (
    AssessmentFactory,
    CompletedModuleFactory,
    DeliverUnitFactory,
    LearnModuleFactory,
    OpportunityAccessFactory,
    OpportunityClaimFactory,
    OpportunityFactory,
    UserVisitFactory,
)
from commcare_connect.users.tests.factories import MobileUserFactory


def test_export_user_visit_data(mobile_user_with_connect_link):
    deliver_unit = DeliverUnitFactory()
    opportunity = OpportunityFactory()
    date1 = now()
    date2 = now()
    UserVisit.objects.bulk_create(
        [
            UserVisit(
                opportunity=opportunity,
                user=mobile_user_with_connect_link,
                visit_date=date1,
                deliver_unit=deliver_unit,
                form_json={"form": {"name": "test_form1"}},
            ),
            UserVisit(
                opportunity=opportunity,
                user=mobile_user_with_connect_link,
                visit_date=date2,
                deliver_unit=deliver_unit,
                entity_id="abc",
                entity_name="A B C",
                form_json={"form": {"name": "test_form2", "group": {"q": "b"}}},
            ),
        ]
    )
    exporter = export_user_visit_data(opportunity, DateRanges.LAST_30_DAYS, [])
    username = mobile_user_with_connect_link.username
    name = mobile_user_with_connect_link.name

    assert exporter.export("csv") == (
        "Visit ID,Visit date,Status,Username,Name of User,Unit Name,Entity ID,Entity Name,form.name,form.group.q\r\n"
        f",{date1.isoformat()},Pending,{username},{name},{deliver_unit.name},,,test_form1,\r\n"
        f",{date2.isoformat()},Pending,{username},{name},{deliver_unit.name},abc,A B C,test_form2,b\r\n"
    )


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {"form": {"name": "form1"}},
            [
                (
                    "form.name",
                    "form1",
                )
            ],
        ),
        ({"form": [{"name": "form1"}, {"name": "form2"}]}, [("form.0.name", "form1"), ("form.1.name", "form2")]),
    ],
)
def test_get_flattened_dataset(data, expected):
    headers = ["header1", "header2"]
    data = [
        ["value1", "value2", data],
    ]
    dataset = get_flattened_dataset(headers, data)
    assert dataset.headers == ["header1", "header2"] + [x[0] for x in expected]
    assert dataset[0] == ("value1", "value2") + tuple(x[1] for x in expected)


def _get_prepared_dataset_for_user_status_test(rows):
    prepared_dataset = Dataset()
    prepared_dataset.headers = (
        "Name",
        "Username",
        "Accepted",
        "Started Learning",
        "Completed Learning",
        "Passed Assessment",
        "Job Claimed",
        "Started Delivery",
        "Last visit date",
    )
    for row in rows:
        prepared_dataset.append(row)
    return prepared_dataset


@pytest.mark.django_db
def test_export_user_status_table_no_data_only(opportunity: Opportunity):
    LearnModuleFactory.create_batch(3, app=opportunity.learn_app)
    mobile_users = MobileUserFactory.create_batch(2)
    rows = []
    for mobile_user in sorted(mobile_users, key=lambda x: x.name):
        date = now()
        OpportunityAccessFactory(opportunity=opportunity, user=mobile_user, accepted=True, date_learn_started=date)
        rows.append((mobile_user.name, mobile_user.username, True, date, "", False, "", "", ""))
    dataset = export_user_status_table(opportunity)
    prepared_test_dataset = _get_prepared_dataset_for_user_status_test(rows)
    assert prepared_test_dataset.export("csv") == dataset.export("csv")


@pytest.mark.django_db
def test_export_user_status_table_learn_data_only(opportunity: Opportunity):
    LearnModuleFactory.create_batch(3, app=opportunity.learn_app)
    mobile_users = MobileUserFactory.create_batch(2)
    rows = []
    for mobile_user in sorted(mobile_users, key=lambda x: x.name):
        date = now()
        OpportunityAccessFactory(opportunity=opportunity, user=mobile_user, accepted=True, date_learn_started=date)
        for learn_module in opportunity.learn_app.learn_modules.all()[2:]:
            CompletedModuleFactory(module=learn_module, user=mobile_user, opportunity=opportunity, date=date)
        rows.append((mobile_user.name, mobile_user.username, True, date, "", False, "", "", ""))
    dataset = export_user_status_table(opportunity)
    prepared_test_dataset = _get_prepared_dataset_for_user_status_test(rows)
    assert prepared_test_dataset.export("csv") == dataset.export("csv")


@pytest.mark.django_db
def test_export_user_status_table_learn_assessment_data_only(opportunity: Opportunity):
    LearnModuleFactory.create_batch(3, app=opportunity.learn_app)
    mobile_users = MobileUserFactory.create_batch(2)
    rows = []
    for mobile_user in sorted(mobile_users, key=lambda x: x.name):
        date = now()
        OpportunityAccessFactory(opportunity=opportunity, user=mobile_user, accepted=True, date_learn_started=date)
        for learn_module in opportunity.learn_app.learn_modules.all():
            CompletedModuleFactory(module=learn_module, user=mobile_user, opportunity=opportunity, date=date)
        AssessmentFactory(app=opportunity.learn_app, opportunity=opportunity, user=mobile_user, passed=True, date=date)
        rows.append((mobile_user.name, mobile_user.username, True, date, date, True, "", "", ""))
    dataset = export_user_status_table(opportunity)
    prepared_test_dataset = _get_prepared_dataset_for_user_status_test(rows)
    assert prepared_test_dataset.export("csv") == dataset.export("csv")


@pytest.mark.django_db
def test_export_user_status_table_data(opportunity: Opportunity):
    LearnModuleFactory.create_batch(3, app=opportunity.learn_app)
    mobile_users = MobileUserFactory.create_batch(2)
    rows = []
    for mobile_user in sorted(mobile_users, key=lambda x: x.name):
        date = now()
        access = OpportunityAccessFactory(
            opportunity=opportunity, user=mobile_user, accepted=True, date_learn_started=date
        )
        OpportunityClaimFactory(opportunity_access=access, max_payments=10, date_claimed=date)
        for learn_module in opportunity.learn_app.learn_modules.all():
            CompletedModuleFactory(module=learn_module, user=mobile_user, opportunity=opportunity, date=date)
        AssessmentFactory(app=opportunity.learn_app, opportunity=opportunity, user=mobile_user, passed=True, date=date)
        UserVisitFactory.create_batch(1, opportunity=opportunity, user=mobile_user, visit_date=date)
        rows.append((mobile_user.name, mobile_user.username, True, date, date, True, date.date(), date, date))
    dataset = export_user_status_table(opportunity)
    prepared_test_dataset = _get_prepared_dataset_for_user_status_test(rows)
    assert prepared_test_dataset.export("csv") == dataset.export("csv")
