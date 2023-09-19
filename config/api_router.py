from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from commcare_connect.form_receiver.views import FormReceiver
from commcare_connect.opportunity.api.views import (
    ClaimOpportunityView,
    OpportunityViewSet,
    UserLearnProgressView,
    UserVisitViewSet,
)
from commcare_connect.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("opportunity", OpportunityViewSet, basename="Opportunity")
router.register("opportunity/(?P<opportunity_id>.+)/deliver_visit", UserVisitViewSet, basename="UserVisit")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("receiver/", FormReceiver.as_view(), name="receiver"),
    path("opportunity/<int:pk>/learn_progress", UserLearnProgressView.as_view(), name="learn_progress"),
    path("opportunity/<int:pk>/claim", ClaimOpportunityView.as_view()),
]
