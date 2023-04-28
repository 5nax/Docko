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
from datetime import  timedelta
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .forms import RegistrationForm, EditProfileForm, scheduleForm
import datetime

def send_confirmation_email(request, booking_id, slotnumber):
    # Get the user information from the request
    user = request.user
    # Define the email subject line
    subject = 'Booking Confirmation'
    # Add a personalized greeting
    greeting = f"Hi {user.first_name},"
    # Construct the confirmation message
    message = f"{greeting}<br><br>We wanted to confirm your booking #{booking_id} on {request.user.userprofile.booked_date.strftime('%A, %B %d, %Y')} at {request.user.userprofile.booked_date.strftime('%I:%M %p')}."

    # Add more details about the booking
    message += "<br><br>Your booking is confirmed and we look forward to seeing you at our location. Please note that if you need to cancel or reschedule your appointment, please let us know at least 24 hours in advance."

    # Add a closing remark
    message += "<br><br>Thank you for choosing our service. If you have any questions or concerns, please don't hesitate to contact us."

    # Define the sender email address
    from_email = 'dockoauto@gmail.com'
    # Define the recipient email address
    recipient_list = [user.email]
    # Send the confirmation email with both plain text and HTML message body
    send_mail(
        subject=subject,
        message='',
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=message
    )

def send_reminder_email(user, booking_id):
    subject = 'Appointment Reminder'
    greeting = f"Hi {user.first_name},"
    message = f"{greeting} This is a reminder that your appointment #{booking_id} is scheduled for tomorrow."
    message += "Please remember to arrive on time and have all necessary documents with you."
    message += "Thank you for choosing our service. If you have any questions or concerns, please don't hesitate to contact us."
    plain_message = strip_tags(message)
    from_email = 'dockoauto@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=message)
def view_profile(request):
    user = request.user
    try:
        profile = user.userprofile
        curr_booking_id = profile.curr_booking_id
        booked_date = profile.booked_date
    except UserProfile.DoesNotExist:
        curr_booking_id = None
        booked_date = None

    args = {
        'user': user,
        'curr_booking_id': curr_booking_id,
        'booked_date': booked_date
    }
    return render(request, 'patient_login/profile.html', args)

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

    def post(self, request, doc_id):
        form = scheduleForm(request.POST)
        doctor = docDetails.objects.get(pk=doc_id)
        curr_user = request.user.userprofile

        def book_slot(slot_number, slot_attr):
            if not getattr(doctor, slot_attr):
                setattr(doctor, slot_attr, True)
                doctor.save()
                return generate_booking_id(slot_number)
            else:
                messages.error(request, 'Already booked!')
                return None

        def generate_booking_id(booked_slot):
            curr_date = datetime.datetime.now().strftime("%d%m%Y")  # returns date in DDMMYYYY format
            doc_pk = f"{doctor.pk:0>2}"  # zero-pads doctor.pk to 2 digits
            user_pk = f"{request.user.pk:0>4}"  # zero-pads request.user.pk to 4 digits
            booking_id = f"BKID{doc_pk}{user_pk}{curr_date}{booked_slot}"
            return booking_id

        if form.is_valid():
            ss = form.cleaned_data['selected_slot']
            slot_mapping = {
                'slot1': ('slot1', 'slot1_id'),
                'slot2': ('slot2', 'slot2_id'),
                'slot3': ('slot3', 'slot3_id'),
                'slot4': ('slot4', 'slot4_id'),
                'slot5': ('slot5', 'slot5_id'),
                'slot6': ('slot6', 'slot6_id'),
                'slot7': ('slot7', 'slot7_id'),
            }

            slot_number, slot_id_attr = slot_mapping[ss]
            booking_id = book_slot(slot_number, slot_number)

            if booking_id is not None:
                setattr(doctor, slot_id_attr, booking_id)
                doctor.save()
                booked_date = form.cleaned_data['date']
                curr_user.curr_booking_id = int(booking_id[10:18])
                curr_user.booked_date = booked_date
                curr_user.save()

                args = {'form': form, 'ss': ss, 'doctor': doctor, 'booked_slot': int(slot_number[-1]),
                        'booking_id': booking_id, 'booked_date': booked_date}  # change booking_date to booked_date
                send_confirmation_email(request, booking_id, slot_number)
                return render(request, 'patient_login/confirmation.html', args)

            args = {'form': form, 'ss': ss, 'doctor': doctor}
            return render(request, self.template_name, args)
        else:
            messages.error(request, 'Form is not valid.')
            args = {'form': form, 'doctor': doctor}
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

    try:
        curr_booking_id = curr_user.userprofile.curr_booking_id
    except UserProfile.DoesNotExist:
        curr_booking_id = None

    if curr_booking_id:
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
