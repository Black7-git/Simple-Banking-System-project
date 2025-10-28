from django.urls import path
from . import views

app_name = "pets"

urlpatterns = [
    path("", views.ReportListView.as_view(), name="report_list"),
    path("report/new/", views.ReportCreateView.as_view(), name="report_create"),
    path("report/<int:pk>/", views.ReportDetailView.as_view(), name="report_detail"),
    path("report/<int:pk>/claim/", views.ClaimCreateView.as_view(), name="claim_create"),
    path("search/", views.SearchView.as_view(), name="search"),
]
