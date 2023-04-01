from django.http import Http404
from doctor_login.models import docDetails
from django.shortcuts import render,redirect
from patient_login.forms import RegistrationForm, EditProfileForm, scheduleForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from  django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import TemplateView
from  .models import UserProfile
import datetime

def view_profile(request):
    args={'user':request.user}
    return render(request,'patient_login/profile.html',args)


class schedule(TemplateView):
    template_name ='schedule.html'

    def get(self,request,doc_id):
        form = scheduleForm()
        try:
            doctor=docDetails.objects.get(pk=doc_id)
            curr_date = datetime.datetime.now().strftime ("%d/%m/%Y")
        except docDetails.DoesNotExist:
            raise Http404("Invalid Doctor Id.")
        return render(request, self.template_name,{'doctor':doctor,'form':form,'curr_date':curr_date})

    def post(self,request,doc_id):
        form =scheduleForm(request.POST)
        doctor = docDetails.objects.get(pk=doc_id)
        curr_user = request.user
        if form.is_valid():

            ss= form.cleaned_data['selected_slot']
            if ss=='slot1':
                if doctor.slot1==False:
                    doctor.slot1 = True
                    doctor.save()
                    booked_slot=1
                    curr_date = datetime.datetime.now().strftime ("%d%m%Y") #returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk))==1:
                        doc_pk='0'+str(doctor.id)
                    elif len(str(doctor.pk))==2:
                        doc_pk=str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk))==1:
                        user_pk = '000'+str(request.user.pk)
                    elif len(str(request.user.pk))==2:
                        user_pk = '00'+str(request.user.pk)
                    elif len(str(request.user.pk))==3:
                        user_pk = '0'+str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)

                    booking_id ='BKID'+doc_pk+ user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor,'booked_slot':booked_slot,'booking_id': booking_id }
                    doctor.slot1_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request,'patient_login/confirmation.html' ,args)
                else:
                    messages.error(request, 'Already  booked !')
            elif ss=='slot2':
                if doctor.slot2 == False:
                    doctor.slot2 = True
                    doctor.save()
                    booked_slot = 2
                    curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk)) == 1:
                        doc_pk = '0' + str(doctor.id)
                    elif len(str(doctor.pk)) == 2:
                        doc_pk = str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk)) == 1:
                        user_pk = '000' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 2:
                        user_pk = '00' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 3:
                        user_pk = '0' + str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)

                    booking_id = 'BKID' + doc_pk + user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': booked_slot,'booking_id': booking_id}
                    doctor.slot2_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request, 'patient_login/confirmation.html', args)
                else:
                    messages.error(request, 'Already  booked !')
            elif ss=='slot3':
                if doctor.slot3 == False:
                    doctor.slot3 = True
                    doctor.save()
                    booked_slot = 3
                    curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk)) == 1:
                        doc_pk = '0' + str(doctor.id)
                    elif len(str(doctor.pk)) == 2:
                        doc_pk = str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk)) == 1:
                        user_pk = '000' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 2:
                        user_pk = '00' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 3:
                        user_pk = '0' + str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)
                    booking_id = 'BKID' + doc_pk + user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': booked_slot,'booking_id': booking_id}
                    doctor.slot3_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request, 'patient_login/confirmation.html', args)
                else:
                    messages.error(request, 'Already  booked !')
            elif ss=='slot4':
                if doctor.slot4 == False:
                    doctor.slot4 = True
                    doctor.save()
                    booked_slot = 4
                    curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk)) == 1:
                        doc_pk = '0' + str(doctor.id)
                    elif len(str(doctor.pk)) == 2:
                        doc_pk = str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk)) == 1:
                        user_pk = '000' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 2:
                        user_pk = '00' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 3:
                        user_pk = '0' + str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)
                    booking_id = 'BKID' + doc_pk + user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': booked_slot,'booking_id': booking_id}
                    doctor.slot4_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request, 'patient_login/confirmation.html', args)
                else:
                    messages.error(request, 'Already  booked !')
            elif ss=='slot5':
                if doctor.slot5 == False:
                    doctor.slot5 = True
                    doctor.save()
                    booked_slot = 5
                    curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk)) == 1:
                        doc_pk = '0' + str(doctor.id)
                    elif len(str(doctor.pk)) == 2:
                        doc_pk = str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk)) == 1:
                        user_pk = '000' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 2:
                        user_pk = '00' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 3:
                        user_pk = '0' + str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)
                    booking_id = 'BKID' + doc_pk + user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': booked_slot,'booking_id': booking_id}
                    doctor.slot5_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request, 'patient_login/confirmation.html', args)
                else:
                    messages.error(request, 'Already  booked !')
            elif ss=='slot6':
                if doctor.slot6 == False:
                    doctor.slot6 = True
                    doctor.save()
                    booked_slot = 6
                    curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk)) == 1:
                        doc_pk = '0' + str(doctor.id)
                    elif len(str(doctor.pk)) == 2:
                        doc_pk = str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk)) == 1:
                        user_pk = '000' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 2:
                        user_pk = '00' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 3:
                        user_pk = '0' + str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)
                    booking_id = 'BKID' + doc_pk + user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': booked_slot,'booking_id': booking_id }
                    doctor.slot6_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request, 'patient_login/confirmation.html', args)
                else:
                    messages.error(request, 'Already  booked !')
            elif ss=='slot7':
                if doctor.slot7 == False:
                    doctor.slot7=True
                    doctor.save()
                    booked_slot = 7
                    curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
                    # adjustment of doctor id for bit 4 and bit 5 of booking id
                    if len(str(doctor.pk)) == 1:
                        doc_pk = '0' + str(doctor.id)
                    elif len(str(doctor.pk)) == 2:
                        doc_pk = str(doctor.id)

                    # adjustment of user id for bits 6,7,8 and 9 of booking id
                    if len(str(request.user.pk)) == 1:
                        user_pk = '000' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 2:
                        user_pk = '00' + str(request.user.pk)
                    elif len(str(request.user.pk)) == 3:
                        user_pk = '0' + str(request.user.pk)
                    else:
                        user_pk = str(request.user.pk)
                    booking_id = 'BKID' + doc_pk + user_pk +str(curr_date)+str(booked_slot)
                    args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': booked_slot,'booking_id': booking_id }
                    doctor.slot7_id = booking_id
                    doctor.save()
                    curr_user.userprofile.curr_booking_id = booking_id
                    curr_user.userprofile.save()
                    return render(request, 'patient_login/confirmation.html', args)
                else:
                    messages.error(request, 'Already  booked !')

        args = {'form':form,'ss':ss,'doctor': doctor,}
        return render(request, self.template_name, args)




def edit_profile(request):
    if request.method =='POST':
        form=EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/patient_login/profile')
    else:
        form= EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request,'patient_login/edit_profile.html',args)


def change_password(request):
    if request.method =='POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/patient_login/profile')
        else:
            return redirect('/patient_login/profile/change_password/')
    else:
        form= PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request,'patient_login/change_password.html',args)

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Registered')
            return redirect('/patient_login/login/')
        else:
            messages.error(request, 'Username already exists')
            return redirect('/patient_login/register/')
    else:
        form=RegistrationForm()
        args={'form':form}
        return render(request, 'patient_login/reg_form.html', args)


def index3(request):
    all_docs = docDetails.objects.all()
    curr_user = request.user
    for docs in all_docs:
        docs.cal_availibity()
    if curr_user.userprofile.curr_booking_id:
        messages.info(request, 'You already have one appointment.')
        return render(request,'patient_login/profile.html')
    else:
        context = {'all_docs':all_docs, 'curr_user':curr_user}
        return render(request, 'list_of_docs.html',context)

def analytics(request):
    all_docs = docDetails.objects.all()
    for docs in all_docs:
        docs.cal_availibity()

    context = {'all_docs':all_docs}
    return render(request, 'analytics.html',context)


def detail(request,doc_id):
    try:
        doctor=docDetails.objects.get(pk=doc_id)
    except docDetails.DoesNotExist:
        raise Http404("Invalid Doctor Id.")
    return render(request, 'doc_details.html',{'doctor': doctor})
