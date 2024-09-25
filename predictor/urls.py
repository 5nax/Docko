from django.urls import path

from patient_login.views import schedule
from . import views

urlpatterns = [
    path('', views.predict_disease, name='predict_disease'),
    path('doctor/<int:doc_id>/schedule/', schedule.as_view(), name='schedule'),

]
