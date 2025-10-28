from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('report-pet/', views.report_pet, name='report_pet'),
    path('pets/<int:pet_id>/request/', views.request_pet, name='request_pet'),
    path('search-lost-pet/', views.search_lost_pet, name='search_lost_pet'),
    path('register/', views.register, name='register'),
    
    # User pages
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
]