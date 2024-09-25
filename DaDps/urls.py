from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('admin_login/', include('admin_login.urls')),
    path('asr/', include('doctor_login.urls')),
    path('patient_login/', include('patient_login.urls')),
    path('doctor_login/', include('doctor_login.urls')),
    path('predictor', include('predictor.urls')),]
