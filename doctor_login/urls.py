from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.doctor_login, name='doctor_login'),
    path('asr/', views.asr, name='asr'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('complete_appointment/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule_appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('view_prescription/<int:appointment_id>/', views.view_prescription, name='view_prescription'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # New URL
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]