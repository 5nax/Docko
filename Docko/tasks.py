from celery import shared_task
from patient_login.models import UserProfile
from datetime import datetime, timedelta

from patient_login.views import send_reminder_email


@shared_task
def send_reminders():
    # Get users with booked_date equal to the next day
    next_day = datetime.now().date() + timedelta(days=1)
    users_with_appointments = UserProfile.objects.filter(booked_date=next_day)

    for user_profile in users_with_appointments:
        send_reminder_email(user_profile.user, user_profile.curr_booking_id)