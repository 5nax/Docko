# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-08 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_login', '0004_auto_20171007_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='images',
            field=models.ImageField(blank=True, upload_to=b'profile_image'),
        ),
    ]
