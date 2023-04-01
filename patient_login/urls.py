from django.urls import re_path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from patient_login.views import schedule

urlpatterns = [
    re_path(r'^$', views.index3, name='index3'),
    re_path(r'^analytics$', views.analytics, name='analytics'),
    re_path(r'^(?P<doc_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^(?P<doc_id>[0-9]+)/schedule/$', schedule.as_view(), name='schedule'),
    re_path(r'^login/$', LoginView.as_view(template_name='patient_login/login.html'), name='login'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^profile/$', views.view_profile, name='view_profile'),
    re_path(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'^profile/change_password/$', PasswordChangeView.as_view(template_name='patient_login/change_password.html', success_url='/patient_login/profile/'), name='change_password'),
    re_path(r'^edit/$', views.edit_profile, name='edit_profile'),
]