from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from . import views

from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetDoneView,
    PasswordResetCompleteView, PasswordResetConfirmView
)
from patient_login.views import (
    index3, analytics, detail, schedule, view_profile,current,
    edit_profile, change_password, register, CustomPasswordResetView
)

urlpatterns = [
    re_path(r'^$', index3, name='index3'),
    re_path(r'^analytics$', analytics, name='analytics'),
    re_path(r'^(?P<doc_id>[0-9]+)/$', detail, name='detail'),
    path('schedule/<int:doc_id>/', schedule.as_view(), name='schedule'),
    re_path(r'^login/$', LoginView.as_view(template_name='patient_login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Add this line
    re_path(r'^register/$', register, name='register'),
    re_path(r'^profile/$', view_profile, name='view_profile'),
    re_path(r'^profile/edit/$', edit_profile, name='edit_profile'),
    path('view_prescription/<int:appointment_id>/', views.patient_view_prescription, name='patient_view_prescription'),

    re_path(r'^current_booking', current, name='current'),
    re_path(r'^profile/change_password/$', PasswordChangeView.as_view(template_name='patient_login/change_password.html', success_url='/patient_login/profile/'), name='change_password'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password-reset/done/$', PasswordResetDoneView.as_view(template_name='patient_login/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^password-reset-complete/$', PasswordResetCompleteView.as_view(template_name='patient_login/password_reset_complete.html'), name='password_reset_complete'),
    re_path(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-_]+)/$', PasswordResetConfirmView.as_view(template_name='patient_login/password_reset_confirm.html'), name='password_reset_confirm')
]
