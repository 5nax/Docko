# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_login', '0005_auto_20171007_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docdetails',
            name='slot1_id',
            field=models.CharField(default='BKID', max_length=19),
        ),
    ]