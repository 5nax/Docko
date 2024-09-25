from django.shortcuts import render
from doctor_login.models import docDetails
from patient_login.models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Appointment, Prescription
from doctor_login.models import docDetails
from .utils import free_slot, assign_slot


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
# Doctor login view
from django.contrib.auth.models import User
def doctor_profile(request):
    # Assuming the user is a doctor and linked to DoctorProfile
    doctor = request.user.doctor_profile
    return render(request, 'doctor_login/doctor_profile.html', {'doctor': doctor})

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        # Try to get the doctor linked to the email
        try:
            doctor = docDetails.objects.get(email=username)
            user = doctor.user  # Get the linked user object
        except docDetails.DoesNotExist:
            return render(request, 'doctor_login/login.html', {'error': 'Doctor not found'})
        except AttributeError:
            return render(request, 'doctor_login/login.html', {'error': 'No user account associated with this doctor'})

        # Authenticate the user using email
        doctor_user = authenticate(request, username=user.username, password=password)
        if doctor_user is not None:
            login(request, doctor_user)
            return redirect('doctor_dashboard')
        else:
            return render(request, 'doctor_login/login.html', {'error': 'Invalid credentials'})

    return render(request, 'doctor_login/login.html')



# doctor_login/views.py

def doctor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    try:
        doctor = request.user.doctor_profile
        # Check if it's the first login
        if doctor.is_first_login:
            messages.info(request, 'Please update your profile and change your password.')
            return redirect('edit_profile')

        appointments = Appointment.objects.filter(doctor=doctor, status='Pending')
        completed_appointments = Appointment.objects.filter(doctor=doctor, status='Complete')
        return render(request, 'doctor_dashboard.html', {
            'appointments': appointments,
            'completed_appointments': completed_appointments
        })
    except docDetails.DoesNotExist:
        return render(request, 'doctor_login/login.html', {'error': 'No doctor profile found for this user.'})


# doctor_login/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment, Prescription
from .forms import PrescriptionForm, PrescriptionItemFormSet

@login_required
def complete_appointment(request, appointment_id):
    # Ensure the appointment exists and is linked to the logged-in doctor
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)

    if appointment.status == 'Complete':
        messages.info(request, 'This appointment has already been marked as complete.')
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        formset = PrescriptionItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Mark the appointment as complete
            appointment.status = 'Complete'
            appointment.save()

            # Create and save the Prescription
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()

            # Associate and save PrescriptionItems
            formset.instance = prescription
            formset.save()

            # Schedule a follow-up appointment if a date is provided
            if prescription.follow_up_date:
                # You can customize the time or other details as needed
                Appointment.objects.create(
                    patient=appointment.patient,
                    doctor=appointment.doctor,
                    date=prescription.follow_up_date,
                    time=appointment.time,  # You might want to allow selecting a new time
                    status='Pending'
                )

            messages.success(request, 'Appointment marked as complete and prescription saved.')
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PrescriptionForm()
        formset = PrescriptionItemFormSet()

    context = {
        'appointment': appointment,
        'form': form,
        'formset': formset,
    }

    return render(request, 'doctor_login/complete_appointment.html', context)


# Cancel an appointment
# doctor_login/views.py

from django.shortcuts import get_object_or_404
from django.contrib import messages

from .utils import free_slot  # Import the helper function


def cancel_appointment(request, appointment_id):
    """
    Cancels an appointment and frees up the corresponding slot.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.status == 'Cancelled':
        messages.info(request, 'This appointment is already cancelled.')
        return redirect('doctor_dashboard')

    appointment.status = 'Cancelled'
    appointment.save()

    # Free the slot associated with this appointment
    doctor = appointment.doctor
    free_slot(doctor, appointment.id)

    messages.success(request, 'Appointment has been successfully cancelled and the slot is now free.')
    return redirect('doctor_dashboard')


# doctor_login/views.py

from .forms import RescheduleAppointmentForm


@login_required
def reschedule_appointment(request, appointment_id):
    """
    Reschedules an appointment by deleting the old one and creating a new one.
    """
    # Fetch the appointment ensuring it belongs to the logged-in doctor
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)

    if appointment.status != 'Pending':
        messages.error(request, 'Only pending appointments can be rescheduled.')
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        form = RescheduleAppointmentForm(request.POST)
        if form.is_valid():
            new_date = form.cleaned_data['new_date']
            new_time = form.cleaned_data.get('new_time')  # Optional

            # Free the current slot
            doctor = appointment.doctor
            free_slot(doctor, appointment.id)

            # Delete the current appointment
            appointment.delete()

            # Create a new appointment
            new_appointment = Appointment.objects.create(
                patient=appointment.patient,
                doctor=doctor,
                date=new_date,
                time=new_time if new_time else appointment.time,
                status='Pending',
            )

            try:
                # Assign a new slot to the new appointment
                assign_slot(doctor, new_appointment)
            except Exception as e:
                messages.error(request, f'Rescheduling failed: {str(e)}')
                # Optionally, you might want to delete the new appointment if slot assignment fails
                new_appointment.delete()
                return redirect('doctor_dashboard')

            messages.success(request, 'Appointment has been successfully rescheduled.')
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RescheduleAppointmentForm(initial={
            'new_date': appointment.date,
            'new_time': appointment.time
        })

    context = {
        'appointment': appointment,
        'form': form,
    }

    return render(request, 'doctor_login/reschedule_appointment.html', context)


# doctor_login/views.py

@login_required
def view_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile, status='Complete')
    try:
        prescription = appointment.prescription
        prescription_items = prescription.items.all()
    except Prescription.DoesNotExist:
        messages.error(request, 'No prescription found for this appointment.')
        return redirect('doctor_dashboard')

    context = {
        'appointment': appointment,
        'prescription': prescription,
        'prescription_items': prescription_items,
    }

    return render(request, 'doctor_login/view_prescription.html', context)
# doctor_login/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DoctorProfileForm, UserForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def edit_profile(request):
    doctor = request.user.doctor_profile
    user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = DoctorProfileForm(request.POST, instance=doctor)
        password_form = CustomPasswordChangeForm(user, request.POST)

        if 'update_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('doctor_profile')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password has been changed successfully.')
                # Check if it's the first login
                if doctor.is_first_login:
                    doctor.is_first_login = False
                    doctor.save()
                return redirect('doctor_profile')
            else:
                messages.error(request, 'Please correct the errors below.')

    else:
        user_form = UserForm(instance=user)
        profile_form = DoctorProfileForm(instance=doctor)
        password_form = CustomPasswordChangeForm(user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'doctor_login/edit_profile.html', context)