# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 07:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_login', '0003_userprofile_curr_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name="curr_booking",
            new_name='curr_booking_id',
        ),
    ]
