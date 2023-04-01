from django import forms
from django.contrib.auth.models import User
from  django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile
from doctor_login.models import docDetails

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone=self.cleaned_data['phone']
            if commit:
                user.save()

            return user

class EditProfileForm(UserChangeForm):
       class Meta:
           model = User
           fields =(
                'email',
                'first_name',
                'last_name',
                'password'
           )
SLOT_LIST=(('slot1','Slot 1'),('slot2','Slot 2'),('slot3','Slot 3'),('slot4','Slot 4'),('slot5','Slot 5'),('slot6','Slot 6'),('slot7','Slot 7'))
class scheduleForm(forms.Form):

    selected_slot= forms.ChoiceField(choices=SLOT_LIST)

