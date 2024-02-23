from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields ="__all__"


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields ="__all__"
        
class ProfileForm(forms.ModelForm):
     
     class Meta:
        model = User
        fields ="__all__"