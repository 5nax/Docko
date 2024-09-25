from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path(r'^$', views.index0, name='index0'),
    re_path(r'^clear-session/$', views.clear_session, name='clear_session'),  # Route to clear session
]
