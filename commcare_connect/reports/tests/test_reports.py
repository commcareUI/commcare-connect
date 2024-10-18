import datetime
import math

import pytest
from factory.faker import Faker

from commcare_connect.conftest import MobileUserFactory
from commcare_connect.opportunity.models import CompletedWorkStatus, Opportunity, VisitValidationStatus
from commcare_connect.opportunity.tests.factories import (
    CompletedWorkFactory,
    DeliverUnitFactory,
    OpportunityAccessFactory,
    PaymentUnitFactory,
    UserVisitFactory,
)
from commcare_connect.reports.views import _get_table_data_for_quarter, _results_to_geojson


@pytest.mark.django_db
def test_delivery_stats(opportunity: Opportunity):
    payment_units = PaymentUnitFactory.create_batch(2, opportunity=opportunity)
    mobile_users = MobileUserFactory.create_batch(5)
    for payment_unit in payment_units:
        DeliverUnitFactory.create_batch(2, payment_unit=payment_unit, app=opportunity.deliver_app, optional=False)
    access_objects = []
    for mobile_user in mobile_users:
        access = OpportunityAccessFactory(user=mobile_user, opportunity=opportunity, accepted=True)
        access_objects.append(access)
        for payment_unit in payment_units:
            completed_work = CompletedWorkFactory(
                opportunity_access=access,
                payment_unit=payment_unit,
                status=CompletedWorkStatus.approved.value,
            )
            for deliver_unit in payment_unit.deliver_units.all():
                UserVisitFactory(
                    opportunity=opportunity,
                    user=mobile_user,
                    deliver_unit=deliver_unit,
                    status=VisitValidationStatus.approved.value,
                    opportunity_access=access,
                    completed_work=completed_work,
                    visit_date=Faker("date_this_month"),
                )

    quarter = math.ceil(datetime.datetime.utcnow().month / 12 * 4)

    # delivery_type filter not applied
    all_data = _get_table_data_for_quarter((datetime.datetime.utcnow().year, quarter), None)
    assert all_data[0]["users"] == 5
    assert all_data[0]["services"] == 10
    assert all_data[0]["beneficiaries"] == 10

    # test delivery_type filter
    filtered_data = _get_table_data_for_quarter(
        (datetime.datetime.utcnow().year, quarter), opportunity.delivery_type.slug
    )
    assert filtered_data == all_data

    # unknown delivery-type should have no data
    unknown_delivery_type_data = _get_table_data_for_quarter((datetime.datetime.utcnow().year, quarter), "unknown")
    assert unknown_delivery_type_data[0]["users"] == 0
    assert unknown_delivery_type_data[0]["services"] == 0
    assert unknown_delivery_type_data[0]["beneficiaries"] == 0


def test_results_to_geojson():
    # Test input
    results = [
        {"gps_location_long": "10.123", "gps_location_lat": "20.456", "status": "approved", "other_field": "value1"},
        {"gps_location_long": "30.789", "gps_location_lat": "40.012", "status": "rejected", "other_field": "value2"},
        {"gps_location_long": "invalid", "gps_location_lat": "50.678", "status": "unknown", "other_field": "value3"},
        {"status": "approved", "other_field": "value4"},  # Case where lat/lon are not present
        {  # Case where lat/lon are null
            "gps_location_long": None,
            "gps_location_lat": None,
            "status": "rejected",
            "other_field": "value5",
        },
    ]

    # Call the function
    geojson = _results_to_geojson(results)

    # Assertions
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 2  # Only the first two results should be included

    # Check the first feature
    feature1 = geojson["features"][0]
    assert feature1["type"] == "Feature"
    assert feature1["geometry"]["type"] == "Point"
    assert feature1["geometry"]["coordinates"] == [10.123, 20.456]
    assert feature1["properties"]["status"] == "approved"
    assert feature1["properties"]["other_field"] == "value1"
    assert feature1["properties"]["color"] == "#00FF00"

    # Check the second feature
    feature2 = geojson["features"][1]
    assert feature2["type"] == "Feature"
    assert feature2["geometry"]["type"] == "Point"
    assert feature2["geometry"]["coordinates"] == [30.789, 40.012]
    assert feature2["properties"]["status"] == "rejected"
    assert feature2["properties"]["other_field"] == "value2"
    assert feature2["properties"]["color"] == "#FF0000"

    # Check that the other cases are not included
    assert all(f["properties"]["other_field"] not in ["value3", "value4", "value5"] for f in geojson["features"])
