from django.urls import path

from commcare_connect.reports import views

app_name = "reports"

urlpatterns = [
    path("program_dashboard", views.program_dashboard_report, name="program_dashboard_report"),
    path("api/visit_map_data/", views.visit_map_data, name="visit_map_data"),
    path("delivery_stats", view=views.DeliveryStatsReportView.as_view(), name="delivery_stats_report"),
]
