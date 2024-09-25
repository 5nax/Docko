from celery.bin.control import status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.views import PasswordResetView
from datetime import datetime
from django.http import Http404
from doctor_login.models import docDetails
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .models import UserProfile
from .forms import RegistrationForm, EditProfileForm, scheduleForm
from doctor_login.models import Appointment  # Import the Appointment model
from django.contrib import messages  # To display messages
from django.core.mail import send_mail  # For sending emails
from datetime import *

class CustomPasswordResetView(PasswordResetView):
    template_name = 'patient_login/password_reset.html'
    form_class = PasswordResetForm


# Helper function to send emails
def send_email(subject, message, recipient_list):
    from_email = 'dockoauto@gmail.com'
    send_mail(subject=subject, message='', from_email=from_email, recipient_list=recipient_list, html_message=message)

def send_confirmation_email(request, booking_id):
    user = request.user
    subject = 'Booking Confirmation'
    message = f"Hi {user.first_name},<br><br>Your booking #{booking_id} is confirmed for {request.session.get('booked_date')}."
    send_email(subject, message, [user.email])

def send_reminder_email(user, booking_id):
    subject = 'Appointment Reminder'
    message = f"Hi {user.first_name},<br><br>This is a reminder for your appointment #{booking_id} tomorrow. Please arrive on time."
    send_email(subject, strip_tags(message), [user.email])

def view_profile(request):
    user = request.user

    # Check if the user has a latest appointment
    user_profile = user.userprofile
    latest_appointment = user_profile.latest_appointment

    # Prepare context
    context = {
        'username': user.username,
        'latest_appointment': latest_appointment,  # Pass the appointment object to the template
        'user': user,  # You can still use the full user object if needed
    }

    return render(request, 'patient_login/profile.html', context)


def current(request):
    user = request.user
    try:
        user_profile = user.userprofile
        appointments = Appointment.objects.filter(patient=user, status__in=['Pending', 'Confirmed', 'Cancelled',
                                                                            'Complete']).order_by('-date', '-time')

        # Calculate end_time for each appointment
        for appointment in appointments:
            if appointment.time:
                appointment.end_time = (
                            datetime.combine(datetime.today(), appointment.time) + timedelta(minutes=60)).time()
            else:
                appointment.end_time = None

        context = {
            'appointments': appointments,
        }
        return render(request, 'patient_login/current_booking.html', context)
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile does not exist.')


# patient_login/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctor_login.models import Appointment, Prescription


@login_required
def patient_view_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user, status='Complete')

    try:
        prescription = appointment.prescription
        prescription_items = prescription.items.all()
    except Prescription.DoesNotExist:
        messages.error(request, 'No prescription found for this appointment.')
        return redirect('patient_dashboard')

    context = {
        'appointment': appointment,
        'prescription': prescription,
        'prescription_items': prescription_items,
    }

    return render(request, 'patient_login/view_prescription.html', context)



class schedule(TemplateView):
    template_name = 'schedule.html'

    def get(self, request, doc_id):
        form = scheduleForm()
        try:
            doctor = docDetails.objects.get(pk=doc_id)
        except docDetails.DoesNotExist:
            raise Http404("Invalid Doctor ID.")

        # Get the selected date from GET parameters; default to today
        date_str = request.GET.get('date')
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format. Showing today's appointments.")
                selected_date = datetime.now().date()
        else:
            selected_date = datetime.now().date()

        # Format curr_date for display
        curr_date_display = selected_date.strftime("%d/%m/%Y")

        # Fetch appointments for the doctor on the selected date
        appointments = Appointment.objects.filter(doctor=doctor, date=selected_date)

        # Define all possible slots
        all_slots = [
            {'number': 1, 'time': '09:00-10:00', 'code': 'slot1'},
            {'number': 2, 'time': '10:00-11:00', 'code': 'slot2'},
            {'number': 3, 'time': '11:00-12:00', 'code': 'slot3'},
            {'number': 4, 'time': '13:00-14:00', 'code': 'slot4'},
            {'number': 5, 'time': '14:00-15:00', 'code': 'slot5'},
            {'number': 6, 'time': '15:00-16:00', 'code': 'slot6'},
            {'number': 7, 'time': '17:00-18:00', 'code': 'slot7'},
        ]

        # Convert appointment times to strings for comparison
        booked_slots = [appointment.time.strftime('%H:%M') for appointment in appointments]

        # Determine which slots are booked
        for slot in all_slots:
            slot_start_time = slot['time'].split('-')[0]  # e.g., '09:00'
            slot['is_booked'] = slot_start_time in booked_slots

        context = {
            'doctor': doctor,
            'form': form,
            'curr_date': curr_date_display,
            'slots': all_slots,
            'today': datetime.now().date(),
        }

        return render(request, self.template_name, context)

    def post(self, request, doc_id):
        form = scheduleForm(request.POST)
        try:
            doctor = docDetails.objects.get(pk=doc_id)
        except docDetails.DoesNotExist:
            raise Http404("Invalid Doctor ID.")

        # Get the selected date from POST data
        date_str = request.POST.get('date')
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format.")
                selected_date = timezone.now().date()
        else:
            selected_date = timezone.now().date()

        if form.is_valid():
            ss = form.cleaned_data['selected_slot']
            booked_date = form.cleaned_data['date']

            # Time slot mapping (adjust according to your actual slot times)
            slot_mapping = {
                'slot1': '09:00',
                'slot2': '10:00',
                'slot3': '11:00',
                'slot4': '13:00',
                'slot5': '14:00',
                'slot6': '15:00',
                'slot7': '17:00',
            }

            slot_time = slot_mapping.get(ss)
            if not slot_time:
                messages.error(request, 'Invalid slot selected.')
                return self.get(request, doc_id)

            # Check if the selected slot is already booked
            if Appointment.objects.filter(doctor=doctor, date=booked_date, time=slot_time).exists():
                messages.error(request, 'This time slot is already booked!')
                return self.get(request, doc_id)  # Reload the page with updated slot statuses

            # Generate booking ID
            booking_id = generate_booking_id(request.user, doctor, ss)

            # Create and save the appointment
            appointment = Appointment.objects.create(
                patient=request.user,  # The current logged-in user as the patient
                doctor=doctor,         # The doctor instance
                date=booked_date,      # The selected booking date
                time=slot_time,        # The selected time slot
                status='Pending'
            )

            # Save the latest appointment in the user's profile
            user_profile = request.user.userprofile
            user_profile.latest_appointment = appointment
            user_profile.save()

            # Send confirmation email
            self.send_confirmation_email(request, booking_id, slot_time, booked_date)

            # Render confirmation page
            return render(request, 'patient_login/confirmation.html', {
                'doctor': doctor,
                'booked_date': booked_date.strftime("%d/%m/%Y"),
                'booked_slot': slot_time,
                'booking_id': booking_id,
                'status': appointment.status,
            })
        else:
            messages.error(request, 'Form submission is invalid.')
            return self.get(request, doc_id)

    def send_confirmation_email(self, request, booking_id, slot_time, booked_date):
        user = request.user
        subject = 'Booking Confirmation'
        message = (
            f"Hi {user.first_name},\n\n"
            f"Your booking #{booking_id} has been confirmed for {booked_date.strftime('%d/%m/%Y')} at {slot_time}.\n"
            "If you need to cancel or reschedule, please contact us 24 hours in advance.\n\n"
            "Thank you for choosing our service."
        )
        from_email = 'dockoauto@gmail.com'
        recipient_list = [user.email]

        # Send the email
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
def generate_booking_id(user, doctor, booked_slot):
    curr_date = datetime.now().strftime("%d%m%Y")
    return f"BKID{doctor.pk:02}{user.pk:04}{curr_date}{booked_slot}"

from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, UserProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/patient_login/profile')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'patient_login/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/patient_login/profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'patient_login/change_password.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Registered')
            return redirect('/patient_login/login/')
    else:
        form = RegistrationForm()
    return render(request, 'patient_login/reg_form.html', {'form': form})

def index3(request):
    all_docs = docDetails.objects.all()
    request.session.update({
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })

    curr_booking_id = getattr(request.user.userprofile, 'curr_booking_id', None)
    request.session['curr_booking_id'] = curr_booking_id

    if curr_booking_id:
        messages.info(request, 'You already have one appointment.')
        return redirect('view_profile')

    return render(request, 'patient_login/profile.html', {'curr_user': request.user})

def analytics(request):
    all_docs = docDetails.objects.all()
    return render(request, 'analytics.html', {'all_docs': all_docs})

def detail(request, doc_id):
    try:
        doctor = docDetails.objects.get(pk=doc_id)
    except docDetails.DoesNotExist:
        raise Http404("Invalid Doctor ID")
    return render(request, 'doc_details.html', {'doctor': doctor})
