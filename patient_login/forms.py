from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from patient_login.models import UserProfile


class scheduleForm(forms.Form):
    selected_slot = forms.ChoiceField(choices=[(f'slot{i}', f'Slot {i}') for i in range(1, 8)], label='Select a time slot')
    date = forms.DateField(label='Select a date', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise forms.ValidationError("You cannot select a past date.")
        return selected_date
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=True, label='Phone Number')
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, label='Gender')

    class Meta:
        model = UserProfile
        fields = ('phone', 'dob', 'gender')