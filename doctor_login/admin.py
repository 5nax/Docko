from django.contrib import admin
from .models import docDetails

@admin.register(docDetails)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'specialization', 'availibity')