# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from datetime import datetime
import datetime

class docDetails(models.Model):
    first_name = models.CharField(max_length=15,default='')
    last_name = models.CharField(max_length=15,default='')
    fees=models.PositiveIntegerField(blank=0,default=0)
    experience=models.PositiveIntegerField(blank=0,default=0)
    Address =models.CharField(max_length=100,default='')
    Landmark = models.CharField(max_length=20, default='')
    City=models.CharField(max_length=15,default='')
    PIN=models.CharField(max_length=6, default='')
    State=models.CharField(max_length=15,default='')
    specialization=models.CharField(max_length=30, default='')
    description=models.CharField(max_length=1000, default='')
    email = models.EmailField(max_length=50,default='')
    phone = models.CharField(max_length=10,default='' )

    slot1 = models.BooleanField(default=False)
    slot2 = models.BooleanField(default=False)
    slot3 = models.BooleanField(default=False)
    slot4 = models.BooleanField(default=False)
    slot5 = models.BooleanField(default=False)
    slot6 = models.BooleanField(default=False)
    slot7 = models.BooleanField(default=False)

    slot1_id = models.CharField(max_length=19, default=0, blank=True )
    slot2_id = models.CharField(max_length=19, default='',blank=True )
    slot3_id = models.CharField(max_length=19, default='',blank=True )
    slot4_id = models.CharField(max_length=19, default='',blank=True )
    slot5_id = models.CharField(max_length=19, default='',blank=True )
    slot6_id = models.CharField(max_length=19, default='',blank=True )
    slot7_id = models.CharField(max_length=19, default='',blank=True )

    availibity = models.FloatField(default=0,blank=True)

    def __str__(self):
        return str (self.pk)+') '+ self.first_name+' '+ self.last_name+' | '+ self.specialization

    def asr(self):
        self.slot1 = False
        self.slot1_id = ''
        self.slot2 = False
        self.slot2_id = ''
        self.slot3 = False
        self.slot3_id = ''
        self.slot4 = False
        self.slot4_id = ''
        self.slot5 = False
        self.slot5_id = ''
        self.slot6 = False
        self.slot6_id = ''
        self.slot7 = False
        self.slot7_id = ''
        self.save()

    def cal_availibity(self):
        count=0.0
        avail=0.0
        if self.slot1:
            count=count+1
        if self.slot2:
            count=count+1
        if self.slot3:
            count=count+1
        if self.slot4:
            count=count+1
        if self.slot5:
            count=count+1
        if self.slot6:
            count=count+1
        if self.slot7:
            count=count+1

        avail=round(100-(count*100/7),2)
        self.availibity=avail
        self.save()

    
