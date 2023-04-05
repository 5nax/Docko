from django.urls import re_path, path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
]