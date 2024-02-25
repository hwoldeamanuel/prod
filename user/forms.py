from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
        
class ProfileForm(forms.ModelForm):
     
     class Meta:
        model = Profile
        fields=['first_name',
            'last_name',
            'portfolio',
            'contact_number',
            'job_title',
            'portfolio',
            'reports_to',
            ]