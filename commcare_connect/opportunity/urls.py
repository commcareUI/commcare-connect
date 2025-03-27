from django.urls import path

from commcare_connect.opportunity import tw_views, views
from commcare_connect.opportunity.views import (
    OpportunityCompletedWorkTable,
    OpportunityCreate,
    OpportunityDeliverStatusTable,
    OpportunityDetail,
    OpportunityEdit,
    OpportunityFinalize,
    OpportunityInit,
    OpportunityLearnStatusTableView,
    OpportunityList,
    OpportunityPaymentTableView,
    OpportunityPaymentUnitTableView,
    OpportunityUserLearnProgress,
    OpportunityUserStatusTableView,
    UserPaymentsTableView,
    add_budget_existing_users,
    add_payment_unit,
    add_payment_units,
    approve_visit,
    delete_form_json_rule,
    download_export,
    edit_payment_unit,
    export_catchment_area,
    export_completed_work,
    export_deliver_status,
    export_status,
    export_user_status,
    export_user_visits,
    export_users_for_payment,
    fetch_attachment,
    get_application,
    import_catchment_area,
    opportunity_user_invite,
    payment_delete,
    payment_import,
    payment_report,
    reject_visit,
    resend_user_invite,
    review_visit_export,
    review_visit_import,
    revoke_user_suspension,
    send_message_mobile_users,
    suspend_user,
    suspended_users_list,
    update_completed_work_status_import,
    update_visit_status_import,
    user_profile,
    user_visit_review,
    user_visits_list,
    verification_flags_config,
    visit_verification,
    worker_deliver,
    worker_learn,
    worker_list,
    worker_verify,
)

app_name = "opportunity"
urlpatterns = [
    path("", view=OpportunityList.as_view(), name="list"),
    path("create/", view=OpportunityCreate.as_view(), name="create"),
    path("init/", view=OpportunityInit.as_view(), name="init"),
    path("<int:pk>/finalize/", view=OpportunityFinalize.as_view(), name="finalize"),
    path("<int:pk>/edit", view=OpportunityEdit.as_view(), name="edit"),
    path("<int:pk>/", view=OpportunityDetail.as_view(), name="detail"),
    path("<int:pk>/user_table/", view=OpportunityLearnStatusTableView.as_view(), name="user_table"),
    path("<int:pk>/user_status_table/", view=OpportunityUserStatusTableView.as_view(), name="user_status_table"),
    path("<int:pk>/visit_export/", view=export_user_visits, name="visit_export"),
    path("<int:pk>/review_visit_export/", view=review_visit_export, name="review_visit_export"),
    path("<int:pk>/review_visit_import/", view=review_visit_import, name="review_visit_import"),
    path("export_status/<slug:task_id>", view=export_status, name="export_status"),
    path("download_export/<slug:task_id>", view=download_export, name="download_export"),
    path("<int:pk>/visit_import/", view=update_visit_status_import, name="visit_import"),
    path(
        "<int:opp_id>/learn_progress/<int:pk>",
        view=OpportunityUserLearnProgress.as_view(),
        name="user_learn_progress",
    ),
    path(
        "<int:pk>/add_budget_existing_users",
        view=add_budget_existing_users,
        name="add_budget_existing_users",
    ),
    path("<int:pk>/payment_table/", view=OpportunityPaymentTableView.as_view(), name="payment_table"),
    path("<int:pk>/payment_export/", view=export_users_for_payment, name="payment_export"),
    path("<int:pk>/payment_import/", view=payment_import, name="payment_import"),
    path("<int:pk>/payment_unit/create", view=add_payment_unit, name="add_payment_unit"),
    path("<int:pk>/payment_units/create", view=add_payment_units, name="add_payment_units"),
    path("<int:pk>/payment_unit_table/", view=OpportunityPaymentUnitTableView.as_view(), name="payment_unit_table"),
    path("<int:opp_id>/payment_unit/<int:pk>/edit", view=edit_payment_unit, name="edit_payment_unit"),
    path("<int:opp_id>/user_payment_table/<int:pk>", view=UserPaymentsTableView.as_view(), name="user_payments_table"),
    path("<int:pk>/user_status_export/", view=export_user_status, name="user_status_export"),
    path("<int:pk>/deliver_status_table/", view=OpportunityDeliverStatusTable.as_view(), name="deliver_status_table"),
    path("<int:pk>/deliver_status_export/", view=export_deliver_status, name="deliver_status_export"),
    path("<int:opp_id>/user_visits/<int:pk>/", view=user_visits_list, name="user_visits_list"),
    path("<int:opp_id>/payment/<int:access_id>/delete/<int:pk>/", view=payment_delete, name="payment_delete"),
    path("<int:opp_id>/user_profile/<int:pk>/", view=user_profile, name="user_profile"),
    path("<int:pk>/send_message", view=send_message_mobile_users, name="send_message_mobile_users"),
    path("applications/", get_application, name="get_applications_by_domain"),
    path("verification/<int:pk>/", view=visit_verification, name="visit_verification"),
    path("approve/<int:pk>/", view=approve_visit, name="approve_visit"),
    path("reject/<int:pk>/", view=reject_visit, name="reject_visit"),
    path("fetch_attachment/<blob_id>", view=fetch_attachment, name="fetch_attachment"),
    path("<int:pk>/completed_work_table/", view=OpportunityCompletedWorkTable.as_view(), name="completed_work_table"),
    path("<int:pk>/completed_work_export/", view=export_completed_work, name="completed_work_export"),
    path("<int:pk>/completed_work_import/", view=update_completed_work_status_import, name="completed_work_import"),
    path("<int:pk>/verification_flags_config/", view=verification_flags_config, name="verification_flags_config"),
    path("<int:pk>/suspended_users/", view=suspended_users_list, name="suspended_users_list"),
    path("<int:opp_id>/suspend_user/<int:pk>/", view=suspend_user, name="suspend_user"),
    path("<int:opp_id>/revoke_user_suspension/<int:pk>/", view=revoke_user_suspension, name="revoke_user_suspension"),
    path("<int:opp_id>/delete_form_json_rule/<int:pk>/", view=delete_form_json_rule, name="delete_form_json_rule"),
    path("<int:opp_id>/workers/list/", view=worker_list, name="worker_list"),
    path("<int:opp_id>/workers/learn/", view=worker_learn, name="worker_learn"),
    path("<int:opp_id>/workers/deliver/", view=worker_deliver, name="worker_deliver"),
    path("<int:opp_id>/workers/verify/", view=worker_verify, name="worker_verify"),
    path("<int:pk>/catchment_area_export/", view=export_catchment_area, name="catchment_area_export"),
    path("<int:pk>/catchment_area_import/", view=import_catchment_area, name="catchment_area_import"),
    path("<int:pk>/payment_report/", payment_report, name="payment_report"),
    path("<int:opp_id>/user_visit_review/", user_visit_review, name="user_visit_review"),
    path("<int:pk>/user_invite/", view=opportunity_user_invite, name="user_invite"),
    path("<int:pk>/invoice/", views.invoice_list, name="invoice_list"),
    path("<int:pk>/invoice_table/", views.PaymentInvoiceTableView.as_view(), name="invoice_table"),
    path("<int:pk>/invoice/create/", views.invoice_create, name="invoice_create"),
    path("<int:pk>/invoice/approve/", views.invoice_approve, name="invoice_approve"),
    path("<int:opp_id>/user_invite_delete/<int:pk>/", views.user_invite_delete, name="user_invite_delete"),
    path("<int:opp_id>/resend_invite/<int:pk>", resend_user_invite, name="resend_user_invite"),
    # New tailwind based views
    path("<int:opp_id>/tw/dashboard/", tw_views.dashboard, name="tw_dashboard"),
    path("<int:opp_id>/tw/worker/", tw_views.worker, name="tw_worker"),
    path("<int:opp_id>/tw/opportunities/", tw_views.opportunities, name="tw_opportunities"),
    path("<int:opp_id>/tw/flagged_workers/", tw_views.flagged_workers, name="tw_flagged_workers"),
    path("<int:opp_id>/tw/visits/", tw_views.opportunity_visits, name="tw_visits"),
]
