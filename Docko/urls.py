from django.urls import include, path, re_path
from django.contrib import admin

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('admin_login/', include('admin_login.urls')),
    path('asr/', include('doctor_login.urls')),
    path('patient_login/', include('patient_login.urls')),
]