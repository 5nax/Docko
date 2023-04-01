from django.shortcuts import render
from doctor_login.models import docDetails
from patient_login.models import UserProfile

def asr(request):
   all_docs = docDetails.objects.all()
   all_users = UserProfile.objects.all()
   for docs in all_docs:
      docs.asr()
   for users in all_users:
       users.asr()
   r=range(1,101)
   context={'r':r}
   return  render(request,'doctor_login/asr.html',context)
