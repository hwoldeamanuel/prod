from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email","username")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
        
class ProfileForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            self.fields['reports_to'].queryset = User.objects.all().exclude(id=user.id)
            self.fields['reports_to'].initial=User.objects.all().exclude(id=user.id).first()
     
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

class ProfileFormAdd(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            self.fields['reports_to'].queryset = User.objects.all().exclude(id=user.id)
            self.fields['reports_to'].initial=User.objects.all().exclude(id=user.id).first()
     
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
class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Ah, ah, ah. You didn't say the magic word!",
        "inactive": "Permission denied",
    }

class BasicUserDataForm(forms.Form):
  error_css_class = 'is-invalid'
  user_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})) 

  class Meta:
    model = User   