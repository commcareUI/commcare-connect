from django.urls import path

from commcare_connect.opportunity.views import (
    OpportunityCreate,
    OpportunityDetail,
    OpportunityEdit,
    OpportunityList,
    OpportunityPaymentTableView,
    OpportunityPaymentUnitTableView,
    OpportunityUserLearnProgress,
    OpportunityUserStatusTableView,
    OpportunityUserTableView,
    OpportunityUserVisitTableView,
    UserPaymentsTableView,
    add_budget_existing_users,
    add_payment_unit,
    download_export,
    edit_payment_unit,
    export_status,
    export_user_visits,
    export_users_for_payment,
    payment_import,
    refresh_app_metadata,
    refresh_app_metadata_status,
    update_visit_status_import,
)

app_name = "opportunity"
urlpatterns = [
    path("", view=OpportunityList.as_view(), name="list"),
    path("create/", view=OpportunityCreate.as_view(), name="create"),
    path("<int:pk>/edit", view=OpportunityEdit.as_view(), name="edit"),
    path("<int:pk>/", view=OpportunityDetail.as_view(), name="detail"),
    path("<int:pk>/user_table/", view=OpportunityUserTableView.as_view(), name="user_table"),
    path("<int:pk>/visit_table/", view=OpportunityUserVisitTableView.as_view(), name="visit_table"),
    path("<int:pk>/user_status_table/", view=OpportunityUserStatusTableView.as_view(), name="user_status_table"),
    path("<int:pk>/visit_export/", view=export_user_visits, name="visit_export"),
    path("export_status/<slug:task_id>", view=export_status, name="export_status"),
    path("download_export/<slug:task_id>", view=download_export, name="download_export"),
    path("<int:pk>/visit_import/", view=update_visit_status_import, name="visit_import"),
    path(
        "<int:opp_id>/learn_progress/<int:pk>", view=OpportunityUserLearnProgress.as_view(), name="user_learn_progress"
    ),
    path("<int:pk>/add_budget_existing_users", view=add_budget_existing_users, name="add_budget_existing_users"),
    path("<int:pk>/payment_table/", view=OpportunityPaymentTableView.as_view(), name="payment_table"),
    path("<int:pk>/payment_export/", view=export_users_for_payment, name="payment_export"),
    path("<int:pk>/payment_import/", view=payment_import, name="payment_import"),
    path("<int:pk>/payment_unit/create", view=add_payment_unit, name="add_payment_unit"),
    path("<int:pk>/payment_unit_table/", view=OpportunityPaymentUnitTableView.as_view(), name="payment_unit_table"),
    path("<int:opp_id>/payment_unit/<int:pk>/edit", view=edit_payment_unit, name="edit_payment_unit"),
    path("<int:opp_id>/user_payment_table/<int:pk>", view=UserPaymentsTableView.as_view(), name="user_payments_table"),
    path("<int:pk>/refresh_apps/", view=refresh_app_metadata, name="refresh_app_metadata"),
    path("refresh_app_status/<slug:task_id>", view=refresh_app_metadata_status, name="refresh_app_metadata_status"),
]
