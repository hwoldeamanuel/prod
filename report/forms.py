from django import forms
from django.core.exceptions import ValidationError
from .models import IcnReport, ActivityReport,IcnReportImpact,ActivityReportImpact, IcnReportImplementationArea,  ActivityReportImplementationArea,IcnReportSubmit, IcnReportDocument, IcnReportSubmitApproval_F, IcnReportSubmitApproval_T, IcnReportSubmitApproval_P, ActivityReportDocument, ActivityReportSubmit,ActivityReportSubmitApproval_F,ActivityReportSubmitApproval_P,ActivityReportSubmitApproval_T
from django import forms

from program.models import  Program, ImplementationArea, Indicator, UserRoles
from conceptnote.models import Icn, Activity, Impact, IcnImplementationArea
from portfolio.models import Portfolio
from datetime import datetime
from django.forms.models import modelformset_factory
from django_select2 import forms as s2forms
from app_admin.models import Country , Region , Zone , Woreda , Approvalf_Status, Approvalt_Status, Submission_Status
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.utils import timezone
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
        icn = kwargs.pop('icn', None)
        super().__init__(*args, **kwargs)
        
        if user and icn:
           
            program = Program.objects.filter(users_role=user)
            icnreport = IcnReport.objects.filter(user=user)

            self.fields['icn'].queryset =  Icn.objects.filter(id=icn.id)
            self.fields['icn'].initial = Icn.objects.filter(id=icn.id).first()
            self.fields['program_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user)
            self.fields['program_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user).first()
            self.fields['technical_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user)
            self.fields['technical_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user).first()
            self.fields['finance_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user)
            self.fields['finance_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user).first()
            self.fields['actual_report_date'].initial= timezone.now()
        myfield = [
            
            'description',
            'actual_start_date', 
            'actual_end_date',
           
            'actual_report_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget',
           
            'actual_cost_sharing_budget',
            'cs_currency',
            'mc_currency', 
            'iworeda',
            
           
            
           
          


           
            

            ]
        for field in myfield:
            self.fields[field].required = True 

        
    

        self.fields['actual_mc_budget'].widget = forms.widgets.NumberInput(
            attrs={
                'type': 'number', 
                'class': 'form-control form-control-sm'
                }
            )
        self.fields['actual_cost_sharing_budget'].widget = forms.widgets.NumberInput(
            attrs={
                'type': 'number', 
                'class': 'form-control form-control-sm'
                }
            )
       
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
                'class': 'form-control',
                'required': 'true'
                }
            )
     
        
        self.fields['actual_report_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 
              
                'class': 'form-control',
                'readonly':'true'
                }
            )
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-contro-sm', 'rows':'3', 'required':'required'  }    )
       
        self.fields['iworeda'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
        self.fields['iworeda'].queryset = ImplementationArea.objects.all()
         
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
           
            'actual_mc_budget',
           
            'actual_cost_sharing_budget',
            
            'iworeda',
            'cs_currency',
            'mc_currency', 
           
           
          


           
            

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
         icnreport = kwargs.pop('icnreport', None)
         sid = kwargs.pop('sid', None)
         super(IcnReportSubmitForm, self).__init__(*args, **kwargs)

         self.fields['document'].choices = [
             (document.pk, document) for document in IcnReportDocument.objects.filter(user=user, icnreport=icnreport)
         ]

         self.fields['submission_status'].choices = [
            (submission_status.id, submission_status.name) for submission_status in Submission_Status.objects.filter(id=sid)
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
         did = kwargs.pop('did', None)
         super(IcnReportApprovalTForm, self).__init__(*args, **kwargs)
       
    
     
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
         ]
          
         if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in IcnReportDocument.objects.none()
         ]
       
         if did == 3:
               self.fields['document'].widget.attrs['readonly'] = True

        
        
    class Meta:
            model = IcnReportSubmitApproval_T
            fields = ('approval_note','approval_status','document')

            exclude=  ['icnreport','user',]
            


class IcnReportApprovalFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         did = kwargs.pop('did', None)
         super(IcnReportApprovalFForm, self).__init__(*args, **kwargs)
       
    
     
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
         ]
          
         if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in IcnReportDocument.objects.none()
         ]
       
         if did == 3:
               self.fields['document'].widget.attrs['readonly'] = True

        
        
    class Meta:
            model = IcnReportSubmitApproval_F
            fields =  ('approval_note','approval_status','document')

            exclude=  ['icnreport','user']

class IcnReportApprovalPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         did = kwargs.pop('did', None)
         super(IcnReportApprovalPForm, self).__init__(*args, **kwargs)
       
    
     
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalf_Status.objects.filter(id=did)
         ]
          
         if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in IcnReportDocument.objects.none()
         ]
       
         if did == 3:
               self.fields['document'].widget.attrs['readonly'] = True

        
    
               
    class Meta:
            model = IcnReportSubmitApproval_P
            fields =  ('approval_note','approval_status','document')

            exclude=  ['icnreport','user']
    
    



class IcnReportImpactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        
       
          


       
        self.fields['actual_impact_pilot'].widget = forms.widgets.NumberInput(
            attrs={
                'type': 'number', 
                'class': 'form-control form-control-sm'
                }
            )
        self.fields['actual_impact_scaleup'].widget = forms.widgets.NumberInput(
            attrs={
                'type': 'number', 
                'class': 'form-control form-control-sm'
                }
            )
        
        self.fields['actual_impact_pilot'].required = True 
        self.fields['actual_impact_scaleup'].required = True 
    class Meta:
        model = IcnReportImpact
        fields = ['actual_impact_pilot' ,'actual_impact_scaleup',
                    ]
       

class ActivityReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        activity = kwargs.pop('activity', None)
        super().__init__(*args, **kwargs)
      
        if user and activity:
            self.fields['activity'].queryset =  Activity.objects.filter(id=activity.id)
            self.fields['activity'].initial = Activity.objects.filter(id=activity.id).first()
            
            program = Program.objects.filter(users_role=user)
            self.fields['program_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user)
            self.fields['program_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True).exclude(user=user).first()
            self.fields['technical_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user)
            self.fields['technical_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user).first()
            self.fields['finance_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user)
            self.fields['finance_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user).first()
            self.fields['actual_reporting_date'].initial= timezone.now()
           
        myfield = ['activity',
           
            'description',
            'actual_start_date', 
            'actual_end_date',
           
            'actual_reporting_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget',
           
            'actual_cost_sharing_budget',
            'cs_currency',
            'mc_currency', 
         
            
            
           
          


           
            

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
                'type': 'date', 
                'class': 'form-control',
                 'readonly':'true'
                }
            )
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-contro-sm', 'rows':'3', 'required':'required'  }    )
       
       
        self.fields['aworeda'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
        self.fields['aworeda'].queryset = ImplementationArea.objects.all()
         
    class Meta:
        model = ActivityReport
        fields=['activity',
            
            'description',
            'actual_start_date', 
            'actual_end_date',
            'aworeda',
            'actual_reporting_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
           
            'actual_mc_budget',
           
            'actual_cost_sharing_budget',
            'cs_currency',
            'mc_currency', 
            
          
           
           
          


           
            

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
         activityreport = kwargs.pop('activityreport', None)
         sid = kwargs.pop('sid', None)
         super(ActivityReportSubmitForm, self).__init__(*args, **kwargs)

         self.fields['document'].choices = [
             (document.pk, document) for document in ActivityReportDocument.objects.filter(user=user, activityreport=activityreport)
         ]

         self.fields['submission_status'].choices = [
            (submission_status.id, submission_status.name) for submission_status in Submission_Status.objects.filter(id=sid)
        ]   
      # invalid input from the client; ignore and fallback to empty City queryset
        
  
    

         self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
         self.fields['submission_note'].required = True 
             
      # invalid input from the client; ignore and fallback to empty City queryset
        
  
    

       
        
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
         did = kwargs.pop('did', None)
         super(ActivityReportApprovalTForm, self).__init__(*args, **kwargs)
       
    
     
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
         ]
          
         if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in ActivityReportDocument.objects.none()
         ]
       
         if did == 3:
               self.fields['document'].widget.attrs['readonly'] = True
        
    class Meta:
            model = ActivityReportSubmitApproval_T
            fields = ('approval_note','approval_status','document')

            exclude=  ['activityreport','user',]

class ActivityReportApprovalPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         did = kwargs.pop('did', None)
         super(ActivityReportApprovalPForm, self).__init__(*args, **kwargs)
       
    
     
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalf_Status.objects.filter(id=did)
         ]
          
         if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in ActivityReportDocument.objects.none()
         ]
       
         if did == 3:
               self.fields['document'].widget.attrs['readonly'] = True
        
        
    class Meta:
            model = ActivityReportSubmitApproval_P
            fields = ('approval_note','approval_status','document')

            exclude=  ['activityreport','user',]

class ActivityReportApprovalFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         did = kwargs.pop('did', None)
         super(ActivityReportApprovalFForm, self).__init__(*args, **kwargs)
       
    
     
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
         ]
          
         if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in ActivityReportDocument.objects.none()
         ]
       
         if did == 3:
               self.fields['document'].widget.attrs['readonly'] = True
        
    class Meta:
            model = ActivityReportSubmitApproval_F
            fields = ('approval_note','approval_status','document')

            exclude=  ['activityreport','user',]