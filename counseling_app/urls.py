# counseling_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Ensure this is the root URL
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('personal_info/', views.personal_info_view, name='personal_info'),
    path('marks_entry/', views.marks_entry_view, name='marks_entry'),
    path('admin_signup/', views.admin_signup, name='admin_signup'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_admins/', views.manage_admins, name='manage_admins'),
    path('monitor_admins/', views.monitor_admins, name='monitor_admins'),
    path('submit_student_info/', views.submit_student_info, name='submit_student_info'),
]
