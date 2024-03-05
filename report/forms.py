from django import forms
from django.core.exceptions import ValidationError
from .models import IcnReport, ActivityReport,IcnReportImpact,ActivityReportImpact, IcnReportImplementationArea,  ActivityReportImplementationArea,IcnReportSubmit, IcnReportDocument, IcnReportSubmitApproval_F, IcnReportSubmitApproval_T, IcnReportSubmitApproval_P, ActivityReportDocument, ActivityReportSubmit,ActivityReportSubmitApproval_F,ActivityReportSubmitApproval_P,ActivityReportSubmitApproval_T
from django import forms

from program.models import  Program, ImplementationArea, Indicator, UserRoles
from portfolio.models import Portfolio
from datetime import datetime
from django.forms.models import modelformset_factory
from django_select2 import forms as s2forms
from app_admin.models import Country , Region , Zone , Woreda 
from django.contrib.auth.models import User
CHOICE1 =(
    ("1", "Low"),
    ("2", "Medium"),
    ("3", "High"),
    
)
CHOICE2 =(
    ("0", "No"),
    ("1", "Yes"),
  
    
)
class IcnReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
           
            program = Program.objects.filter(users_role=user)
            self.fields['program_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user)
            self.fields['program_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user).first()
            self.fields['technical_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user)
            self.fields['technical_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user).first()
            self.fields['finance_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user)
            self.fields['finance_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user).first()
           
        myfield = [
            
            'description',
            'actual_start_date', 
            'actual_end_date',
            'ilead_agency',
            'actual_report_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget_usd',
           
            'actual_cost_sharing_budget_usd',
            
           
            
           
          


           
            

            ]
        for field in myfield:
            self.fields[field].required = True 

        
    

       
       
        self.fields['actual_start_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
                'required': 'true'
                
                
                }
            )
  
        self.fields['actual_end_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['actual_report_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-contro-sm', 'rows':'3', 'required':'required'  }    )
       
        self.fields['ilead_co_agency'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
        self.fields['ilead_co_agency'].queryset = Portfolio.objects.all()
         
    class Meta:
        model = IcnReport
        fields=['icn',
            
            'description',
            'actual_start_date', 
            'actual_end_date',
            
            'actual_report_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget_usd',
           
            'actual_cost_sharing_budget_usd',
            
           
            'ilead_agency',
            'ilead_co_agency',
           
          


           
            

            ]

        exclude=  ['status', 'approval_status',  'user',]
        
    def clean(self):
         cleaned_data = super().clean()
         
         program_lead = self.cleaned_data.get('program_lead')
         finance_lead = self.cleaned_data.get('finance_lead')
         technical_lead = self.cleaned_data.get('technical_lead')
         
         actual_start_date = self.cleaned_data.get('actual_start_date')
         actual_end_date = self.cleaned_data.get('actual_end_date')
         actual_reporting_date = self.cleaned_data.get('actual_reporting_date')

         if (technical_lead==program_lead or technical_lead==finance_lead):
              self._errors['technical_lead'] = self.error_class(['Lead should take up only one role'])
         elif (program_lead==technical_lead or program_lead==finance_lead):
              self._errors['program_lead'] = self.error_class(['Lead should take up only one role'])
         
         elif (finance_lead==technical_lead or finance_lead==program_lead):
              self._errors['finance_lead'] = self.error_class(['Lead should take up only one role'])
        
         elif ( actual_end_date != None and actual_start_date != None and actual_end_date < actual_start_date):
               self._errors['actual_end_date'] = self.error_class(['End date should always be after start date'])
         elif (actual_reporting_date != None and actual_end_date != None and actual_reporting_date < actual_end_date):
             self._errors['actual_reporting_date'] = self.error_class(['Reporting Date should always be after end date'])
         return cleaned_data








class IcnReportAreaFormEdit(forms.ModelForm):
    
    class Meta:
        model = IcnReportImplementationArea
        fields=['region',
            'zone',
            'woreda',
            ]
        exclude=  ['icnreport']

class IcnReportAreaFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['region'].queryset = Region.objects.all()

        self.fields['zone'].queryset = Zone.objects.none()
        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'region' in self.data:
            try:
                region = int(self.data.get('region'))
                self.fields['zone'].queryset = Zone.objects.filter(region_id=region).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['zone'].queryset = self.instance.region.zone_set.order_by('name')

        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'zone' in self.data:
            try:
                zone = int(self.data.get('zone'))
                self.fields['woreda'].queryset = Woreda.objects.filter(zone_id=zone).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['woreda'].queryset = self.instance.zone.woreda_set.order_by('name')

        myfield = ['region',
            'zone','woreda'          

            ]
        for field in myfield:
            self.fields[field].required = True 
    
    class Meta:
            model = IcnReportImplementationArea
            fields=['region',
            'zone',
            'woreda',
            ]
            exclude=  ['icnreport']

class IcnReportSubmitForm(forms.ModelForm):
     #document = forms.ChoiceField(
         #choices=[(document.id, document.document) for document in Document.objects.all()]
#)

     def __init__(self, *args, **kwargs):
         user = kwargs.pop('user', None)
         icn = kwargs.pop('icn', None)
         super(IcnSubmitForm, self).__init__(*args, **kwargs)

         self.fields['document'].choices = [
             (document.pk, document) for document in IcnReportDocument.objects.filter(user=user, icn=icn)
         ]
             
      # invalid input from the client; ignore and fallback to empty City queryset
        
  
    

         self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
         self.fields['submission_note'].required = True 
        
     class Meta:
            model = IcnReportSubmit
            fields=['submission_status',
            'submission_note',
            'document',
           
           
            ]
            exclude=  ['icnreport',]
            
          


class IcnReportDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
              
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
        self.fields['description'].required = True 
        self.fields['document'].required = True 
    
    
        
    class Meta:
        model = IcnReportDocument
        fields = ('description', 'document',)

        exclude=  ['icn','user', 'ver']


class IcnReportApprovalTForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
        
        
    class Meta:
            model = IcnReportSubmitApproval_T
            fields = ('approval_note','approval_status','document')

            exclude=  ['icnreport','user',]
            


class IcnReportApprovalFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
        
        
    class Meta:
            model = IcnReportSubmitApproval_F
            fields =  ('approval_note','approval_status','document')

            exclude=  ['icnreport','user']

class IcnReportApprovalPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
        
    
               
    class Meta:
            model = IcnReportSubmitApproval_P
            fields =  ('approval_note','approval_status','document')

            exclude=  ['icnreport','user']
    
    



class IcnReportImpactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)
    

       
       
       
        
        self.fields['actual_impact_pilot'].required = True 
        self.fields['actual_impact_scaleup'].required = True 
    class Meta:
        model = IcnReportImpact
        fields = ['actual_impact_pilot' ,'actual_impact_scaleup',
                    ]
        exclude=  ['icnreport']

class ActivityReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            
            program = Program.objects.filter(users_role=user)
            self.fields['program_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user)
            self.fields['program_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user).first()
            self.fields['technical_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user)
            self.fields['technical_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user).first()
            self.fields['finance_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user)
            self.fields['finance_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user).first()
       
           
        myfield = ['activity',
            'icnreport',
            'description',
            'actual_start_date', 
            'actual_end_date',
            'alead_agency',
            'actual_reporting_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget_usd',
           
            'actual_cost_sharing_budget_usd',
            
            
            
           
          


           
            

            ]
        for field in myfield:
            self.fields[field].required = True 

        
    

       
       
        self.fields['actual_start_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
                'required': 'true'
                
                
                }
            )
  
        self.fields['actual_end_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['actual_reporting_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-contro-sm', 'rows':'3', 'required':'required'  }    )
       
        self.fields['alead_co_agency'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
        self.fields['alead_co_agency'].queryset = Portfolio.objects.all()
         
    class Meta:
        model = ActivityReport
        fields=['activity',
            'icnreport',
            'description',
            'actual_start_date', 
            'actual_end_date',
            
            'actual_reporting_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget_usd',
           
            'actual_cost_sharing_budget_usd',
            
          
            'alead_agency',
            'alead_co_agency',
           
          


           
            

            ]

        exclude=  ['status', 'approval_status',  'user',]
        
    def clean(self):
         cleaned_data = super().clean()
         
         program_lead = self.cleaned_data.get('program_lead')
         finance_lead = self.cleaned_data.get('finance_lead')
         technical_lead = self.cleaned_data.get('technical_lead')
         
         actual_start_date = self.cleaned_data.get('actual_start_date')
         actual_end_date = self.cleaned_data.get('actual_end_date')
         actual_reporting_date = self.cleaned_data.get('actual_report_due_date')

         if (technical_lead==program_lead or technical_lead==finance_lead):
              self._errors['technical_lead'] = self.error_class(['Lead should take up only one role'])
         elif (program_lead==technical_lead or program_lead==finance_lead):
              self._errors['program_lead'] = self.error_class(['Lead should take up only one role'])
         
         elif (finance_lead==technical_lead or finance_lead==program_lead):
              self._errors['finance_lead'] = self.error_class(['Lead should take up only one role'])
        
         elif ( actual_end_date != None and actual_start_date != None and actual_end_date < actual_start_date):
               self._errors['actual_end_date'] = self.error_class(['End date should always be after start date'])
         elif (actual_reporting_date != None and actual_end_date != None and actual_reporting_date < actual_end_date):
             self._errors['actual_reporting_date'] = self.error_class(['Reporting Date should always be after end date'])
         return cleaned_data

class ActivityReportAreaFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['region'].queryset = Region.objects.all()

        self.fields['zone'].queryset = Zone.objects.none()
        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'region' in self.data:
            try:
                region = int(self.data.get('region'))
                self.fields['zone'].queryset = Zone.objects.filter(region_id=region).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['zone'].queryset = self.instance.region.zone_set.order_by('name')

        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'zone' in self.data:
            try:
                zone = int(self.data.get('zone'))
                self.fields['woreda'].queryset = Woreda.objects.filter(zone_id=zone).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['woreda'].queryset = self.instance.zone.woreda_set.order_by('name')

        myfield = ['region',
            'zone','woreda'          

            ]
        for field in myfield:
            self.fields[field].required = True 
    
    class Meta:
            model = ActivityReportImplementationArea
            fields=['region',
            'zone',
            'woreda',
            ]
            exclude=  ['activityreport']

class ActivityReportImpactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        icn = kwargs.pop('icn', None)
        super().__init__(*args, **kwargs)
    


       
        self.fields['actual_impact_pilot'].required = True 
        self.fields['actual_impact_scaleup'].required = True 
    class Meta:
        model = ActivityReportImpact
        fields = [ 'actual_impact_pilot' ,'actual_impact_scaleup',
                    ]
        exclude=  ['activityreport']

class ActivityReportSubmitForm(forms.ModelForm):
     #document = forms.ChoiceField(
         #choices=[(document.id, document.document) for document in Document.objects.all()]
#)

     def __init__(self, *args, **kwargs):
         user = kwargs.pop('user', None)
         activity = kwargs.pop('activity', None)
         super(ActivityReportSubmitForm, self).__init__(*args, **kwargs)

         self.fields['document'].choices = [
             (document.pk, document) for document in ActivityReportDocument.objects.filter(user=user, activityreport=activityreport)
         ]
             
      # invalid input from the client; ignore and fallback to empty City queryset
        
  
    

         self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
         self.fields['submission_note'].required = True 
        
     class Meta:
            model = ActivityReportSubmit
            fields=['submission_status',
            'submission_note',
            'document',
           
           
            ]
            exclude=  ['activityreport',]
            
          


class ActivityReportDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
              
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
        self.fields['description'].required = True 
        self.fields['document'].required = True 
    
    
        
    class Meta:
        model = ActivityReportDocument
        fields = ('description', 'document',)

        exclude=  ['activityreport','user', 'ver']

class ActivityReportApprovalTForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
        
        
    class Meta:
            model = ActivityReportSubmitApproval_T
            fields = ('approval_note','approval_status','document')

            exclude=  ['activityreport','user',]

class ActivityReportApprovalPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
        
        
    class Meta:
            model = ActivityReportSubmitApproval_P
            fields = ('approval_note','approval_status','document')

            exclude=  ['activityreport','user',]

class ActivityReportApprovalFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
        
        
    class Meta:
            model = ActivityReportSubmitApproval_F
            fields = ('approval_note','approval_status','document')

            exclude=  ['activityreport','user',]