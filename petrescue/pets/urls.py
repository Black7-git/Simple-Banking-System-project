from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pets/', views.pet_list_view, name='list'),
    path('pets/<int:pet_id>/', views.pet_detail_view, name='detail'),
    path('report/', views.report_pet_view, name='report'),
    path('my-reports/', views.my_reports_view, name='my_reports'),
    path('my-requests/', views.my_requests_view, name='my_requests'),
]