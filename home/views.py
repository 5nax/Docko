from django.http import HttpResponse
from django.shortcuts import render

def index0(request):
   return  render(request,'home/homepage.html')
