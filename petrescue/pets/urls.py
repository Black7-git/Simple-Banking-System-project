from django.urls import path
from . import views

app_name = "pets"

urlpatterns = [
    path("", views.home, name="home"),
    path("report/new/", views.create_report, name="report_create"),
    path("report/<str:reference_code>/", views.report_detail, name="report_detail"),
    path("search/", views.search_reports, name="search"),
]