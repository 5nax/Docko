# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 04:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_login', '0008_auto_20171007_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docdetails',
            name='slot2_id',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
        migrations.AlterField(
            model_name='docdetails',
            name='slot3_id',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
        migrations.AlterField(
            model_name='docdetails',
            name='slot4_id',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
        migrations.AlterField(
            model_name='docdetails',
            name='slot5_id',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
        migrations.AlterField(
            model_name='docdetails',
            name='slot6_id',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
        migrations.AlterField(
            model_name='docdetails',
            name='slot7_id',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
    ]