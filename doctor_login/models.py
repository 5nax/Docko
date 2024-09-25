# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
from datetime import datetime
import datetime

class docDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', default=1)
    first_name = models.CharField(max_length=15, default='')
    last_name = models.CharField(max_length=15, default='')
    fees = models.PositiveIntegerField(blank=True, default=0)
    experience = models.PositiveIntegerField(blank=True, default=0)
    Address = models.CharField(max_length=100, default='')
    Landmark = models.CharField(max_length=20, default='')
    City = models.CharField(max_length=15, default='')
    PIN = models.CharField(max_length=6, default='')
    State = models.CharField(max_length=15, default='')
    specialization = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=1000, default='')
    email = models.EmailField(max_length=50, default='')
    phone = models.CharField(max_length=10, default='')

    slot1 = models.BooleanField(default=False)
    slot2 = models.BooleanField(default=False)
    slot3 = models.BooleanField(default=False)
    slot4 = models.BooleanField(default=False)
    slot5 = models.BooleanField(default=False)
    slot6 = models.BooleanField(default=False)
    slot7 = models.BooleanField(default=False)

    slot1_id = models.CharField(max_length=19, default=0, blank=True)
    slot2_id = models.CharField(max_length=19, default='', blank=True)
    slot3_id = models.CharField(max_length=19, default='', blank=True)
    slot4_id = models.CharField(max_length=19, default='', blank=True)
    slot5_id = models.CharField(max_length=19, default='', blank=True)
    slot6_id = models.CharField(max_length=19, default='', blank=True)
    slot7_id = models.CharField(max_length=19, default='', blank=True)

    availibity = models.FloatField(default=0, blank=True)
    is_first_login = models.BooleanField(default=True)  # New field

    def __str__(self):
        return f"{self.pk}) {self.first_name} {self.last_name} | {self.specialization}"

    def asr(self):
        # Reset all slots
        for i in range(1, 8):
            setattr(self, f'slot{i}', False)
            setattr(self, f'slot{i}_id', '')
        self.save()

    def cal_availibity(self):
        count = sum([
            self.slot1, self.slot2, self.slot3,
            self.slot4, self.slot5, self.slot6, self.slot7
        ])
        self.availibity = round(100 - (count * 100 / 7), 2)
        self.save()

class Appointment(models.Model):

    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(docDetails, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('Cancelled', 'Cancelled')])

    def __str__(self):
        return f"Appointment {self.id} - {self.patient.first_name} with Dr. {self.doctor.first_name} {self.doctor.last_name}"

# doctor_login/models.py

from django.db import models


class Prescription(models.Model):
    appointment = models.OneToOneField('Appointment', on_delete=models.CASCADE)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)  # Optional notes
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Prescription for {self.appointment}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)  # e.g., "2 pills"
    frequency = models.CharField(max_length=50)  # e.g., "twice a day"
    duration_months = models.PositiveIntegerField()  # e.g., 3 for 3 months

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage} - {self.frequency} for {self.duration_months} months"