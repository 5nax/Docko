from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime, timedelta

gender_list = (('male','Male'),('female','Female'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(default=0)
    dob = models.DateField(default=datetime.now)
    gender = models.CharField(choices=gender_list,max_length=6)
    booked_date = models.DateField(null=True, blank=True)
    curr_booking_id = models.IntegerField(default=0)


    def __str__(self):
        return str (self.pk)+')'+' '+self.user.username

    def asr(self):
        self.curr_booking_id = 0
        self.save()

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

