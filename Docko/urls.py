from django.contrib import admin
from django.urls import path , include
from chatbot.views import chatbot
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('admin_login/', include('admin_login.urls')),
    path('asr/', include('doctor_login.urls')),
    path('patient_login/', include('patient_login.urls')),
    path('',include('chatbot.urls')),

]