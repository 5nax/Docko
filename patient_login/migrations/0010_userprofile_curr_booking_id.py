# Generated by Django 4.2 on 2023-04-28 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_login', '0009_rename_booking_date_userprofile_booked_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='curr_booking_id',
            field=models.IntegerField(default=0),
        ),
    ]
