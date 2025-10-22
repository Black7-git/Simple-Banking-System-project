"""
URL configuration for pets app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Home and basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Pet management
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/report/', views.report_pet, name='report_pet'),
    path('pets/<int:pk>/edit/', views.edit_pet, name='edit_pet'),
    path('pets/<int:pk>/delete/', views.delete_pet, name='delete_pet'),
    
    # Request management
    path('requests/', views.request_list, name='request_list'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    
    # Admin
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin/requests/<int:pk>/update/', views.admin_update_request, name='admin_update_request'),
    path('admin/pets/<int:pk>/verify/', views.admin_verify_pet, name='admin_verify_pet'),
]
