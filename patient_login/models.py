from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime



class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(default=0)
    dob = models.DateField(default=datetime.now)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)  # max_length=1 to match choice keys

    # Linking to the latest appointment
    latest_appointment = models.ForeignKey('doctor_login.Appointment', null=True, blank=True, on_delete=models.SET_NULL,
                                           related_name='latest_appointment')

    def __str__(self):
        return str(self.pk) + ')' + ' ' + self.user.username

    def asr(self):
        self.latest_appointment = None
        self.save()


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
