# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-27 05:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_login', '0015_auto_20171027_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docdetails',
            name='current_date',
        ),
    ]
