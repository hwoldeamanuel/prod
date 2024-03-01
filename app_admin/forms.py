from django import forms
from django.contrib.auth.models import User
from .models import Region, Zone, Woreda, Portfolio_Category, Portfolio_Type
from django.contrib.auth.models import Group, Permission
from django_select2 import forms as s2forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import Profile
from program.models import Program, UserRoles

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields =  ("username","email",)




class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = User
        fields = ['avatar', 'bio']

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields =  ("email",)

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            self.fields['reports_to'].queryset = User.objects.all().exclude(id=user.id)
            self.fields['reports_to'].initial=User.objects.all().exclude(id=user.id).first()
    
        
    
    class Meta:
        model = Profile
        fields="__all__"
        exclude=['user']
     
     
class WoredaForm(forms.ModelForm):  
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['zone'].queryset = Zone.objects.filter(region_id=1)
       
        if 'region' in self.data:
            try:
                region = int(self.data.get('region'))
                self.fields['zone'].queryset = Zone.objects.filter(region_id=region).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        
    
    
    class Meta:
        model = Woreda
        fields=['name',]
    
class WoredaFormE(forms.ModelForm): 
      
      class Meta:
        model = Woreda
        fields=['name']

class ZoneFormE(forms.ModelForm): 
      
      class Meta:
        model = Woreda
        fields=['name']
        
class RegionForm(forms.ModelForm): 
      class Meta:
        model = Region
        fields="__all__"

class ZoneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['region'].queryset = Region.objects.all()
    class Meta:
        model = Zone
        fields=['region','name',]           
      # invalid input from the client; ignore and fallback to empty City queryset
        

class TypeForm(forms.ModelForm):
    class Meta:
        model = Portfolio_Type
        fields="__all__"  


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Portfolio_Category
        fields="__all__"  


class UserGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
    

        self.fields['groups'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select', 'data-width': '100%'})
        self.fields['groups'].queryset = Group.objects.all()
    class Meta:
        model = User
        fields=[
                'groups',
                ]
     

class GroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        self.fields['permissions'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select', 'data-width': '100%'})
        self.fields['permissions'].queryset = Permission.objects.all()

    class Meta:
        model = Group
        fields=['permissions']

class GroupAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        self.fields['permissions'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select', 'data-width': '100%'})
        self.fields['permissions'].queryset = Permission.objects.all()

    class Meta:
        model = Group
        fields=['name','permissions']

class UserRoleFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)
        
        if program:
            self.fields['program'].queryset = Program.objects.filter(title=program)
    
    class Meta:
        model = UserRoles
        fields=['program','is_pcn_initiator', 'is_pcn_technical_approver', 'is_pcn_program_approver','is_pcn_finance_approver']


class UserProgramRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            
            self.fields['program'].queryset = Program.objects.exclude(users_role__in=user)
            Program.objects.exclude(users_role__in=user)
        else:
           
            self.fields['program'].queryset = Program.objects.all()
        
            
    class Meta:
        model = UserRoles
        fields=['program','is_pcn_initiator', 'is_pcn_technical_approver', 'is_pcn_program_approver','is_pcn_finance_approver']
