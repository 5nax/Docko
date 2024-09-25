# doctor_login/forms.py

from django import forms
from .models import Prescription, PrescriptionItem
from django.forms import inlineformset_factory
from django import forms
from .models import Appointment
from django.forms import ModelForm
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from .models import docDetails
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

class PrescriptionForm(forms.ModelForm):
    follow_up_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        required=False,
        label="Follow-up Date"
    )

    class Meta:
        model = Prescription
        fields = ['follow_up_date']

class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine_name', 'dosage', 'frequency', 'duration_months']

# Create an inline formset for PrescriptionItems
PrescriptionItemFormSet = inlineformset_factory(
    Prescription,
    PrescriptionItem,
    form=PrescriptionItemForm,
    extra=3,  # Number of empty forms to display
    can_delete=False
)


class RescheduleAppointmentForm(forms.ModelForm):


    new_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="New Date",
        required=True
    )
    # Optionally, add a new_time field if you want to allow changing the time
    new_time = forms.TimeField(
         widget=forms.TimeInput(format='%H:%M'),
         label="New Time",
         required=False
     )

    class Meta:
        model = Appointment
        fields = ['new_date']  # Include 'new_time' if added


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = docDetails
        fields = [
            'fees', 'experience', 'Address', 'Landmark',
            'City', 'PIN', 'State', 'specialization',
            'description', 'phone'
        ]

class CustomPasswordChangeForm(DjangoPasswordChangeForm):
    # You can customize the form if needed
    pass