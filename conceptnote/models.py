from django.db import models
from program.models import  Program, Indicator, UserRoles
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_delete,pre_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
import os
from django.db.models import Max, Avg,Sum,Count,F
from uuid import uuid4
# Create your models here.
from app_admin.models import Country as NCountry, Region as NRegion, Zone as NZone, Woreda as NWoreda, Approvalt_Status, Approvalf_Status, Submission_Status
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from program.models import ImplementationArea

class Icn(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)
    proposed_start_date = models.DateField()
    proposed_end_date = models.DateField()
    
    ilead_agency = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='icns')
    ilead_co_agency = models.ManyToManyField(Portfolio,  blank=True, related_name='co_leads')
    final_report_due_date = models.DateField(null=True, blank=True)
    program_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='iprogram_lead')
    technical_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='itechnical_lead')
    finance_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='ifinance_lead')
    description = models.TextField(null=True, blank=True)
    iworeda = models.ManyToManyField(ImplementationArea,  blank=True, related_name='program_woredas')
    
    mc_budget = models.FloatField(null=True, blank=True)
    
    cost_sharing_budget = models.FloatField(null=True, blank=True)
    icn_number =  models.CharField(max_length=100, null=True, blank=True)
    eniromental_impact =  models.CharField(max_length=255, null=True, blank=True)
    
    environmental_assessment_att = models.FileField(null=True,  blank=True, upload_to='documents/')
    USD = 1
    ETB = 2
    CURRENCY_CHOICES =   (
        (USD, 'USD'),
        (ETB, 'ETB'),
     
        )

    STATUS_CHOICES = [(False, 'Draft'), (True, 'Submitted')]
    mc_currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
    cs_currency =  models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
    status = models.BooleanField("Status", default=False, 
                                    choices=STATUS_CHOICES)
    approval_status = models.CharField(max_length=100,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

    
    
    def save(self,*args, **kwargs):
        suffix = f"{self.pk}".zfill(4)
        self.icn_number = f"{self.program.title}/ICN/{suffix}"
        super(Icn, self).save(*args, **kwargs)

   
    

    def get_num_indicator(self):
        if Impact.objects.filter(icn_id=self).exists():
            qs = Icn.objects.filter(title=self).annotate(Count('impact', distinct=True), Count('impact__indicators', distinct=True))
            num = qs[0].impact__indicators__count
        else:
            num = 0
       
        
        return num
    def get_name(self):
        return "Intervention"
    
   
    def __str__(self):
        return self.title
  

class IcnImplementationArea(models.Model):
    icn =  models.ForeignKey(
        Icn, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        NRegion, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(
        NZone, on_delete=models.CASCADE, null=True, blank=True)
    woreda = models.OneToOneField(NWoreda, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

def path_and_rename(instance, filename):
    upload_to = 'documents/'
    ext = filename.split('.')[-1]

    # get filename
    if hasattr(instance, 'icn'):
        filename = '{}.{}'.format(instance.icn.title +"_Version_"+ instance.ver + "_" + instance.user.username, ext)
    elif hasattr(instance, 'activity'):
         filename = '{}.{}'.format(instance.activity.title +"_Version_"+ instance.ver + "_" + instance.user.username, ext)
        # set filename as random string
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
    

class Document(models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='uploaded_by')
    icn = models.ForeignKey(Icn, on_delete=models.CASCADE,  blank=True)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(null=True,  blank=True, max_length=500, upload_to=path_and_rename)
    ver = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)

    class Meta:
        ordering = ('-uploaded_at',)
    
    
    
    def __str__(self):
        return "%s %s %s" % ("Version", self.ver, self.user.username)
    
      

    
    
    

class IcnSubmit(models.Model):
   
    id = models.AutoField(primary_key=True)
    icn =  models.ForeignKey(
        Icn, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    submission_status = models.ForeignKey(Submission_Status, on_delete=models.CASCADE)
    submission_note = models.TextField(null=True,  blank=True)

    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ('-submission_date',)
    
    
    def save(self, *args, **kwargs):
        if self.submission_date and self.old_submission_date != self.submission_date:
            self.submission_date = timezone.now()
        super(IcnSubmit, self).save(*args, **kwargs)
   
    
    def __str__(self):
        return str(self.id)
    

class Icn_Approval(models.Model):
    Pending_Review = 1
    Require_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending_Review'),
        (Require_Update, 'Require Update'),
        (Approved, 'Approved'),
        (Rejected, 'Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.PositiveSmallIntegerField(choices=STATUS, default=1, blank=True, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.approval_date and self.old_approval_date != self.approval_date:
            self.approval_date = timezone.now()
        super(Icn_Approval, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)

class IcnSubmitApproval_T(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Endorsed'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(IcnSubmitApproval_T, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnSubmitApproval_T, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)
    

class IcnSubmitApproval_P(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Approved'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE ,null=True,  blank=True)
    
    def __init__(self, *args, **kwargs):
        super(IcnSubmitApproval_P, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnSubmitApproval_P, self).save(*args, **kwargs)

 
        
    def __str__(self):
        return str(self.id)

class IcnSubmitApproval_F(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Endorsed'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(IcnSubmitApproval_F, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnSubmitApproval_F, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.id)
    


class Impact(models.Model):
    icn =  models.ForeignKey(
        Icn, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    impact_pilot  = models.IntegerField(null=True, blank=True)
    impact_scaleup  = models.IntegerField(null=True, blank=True)
    indicators = models.ManyToManyField(Indicator, related_name='impacts')

    def __str__(self):
        return str(self.title)

class Activity(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    icn = models.ForeignKey(Icn, on_delete=models.DO_NOTHING)
    proposed_start_date = models.DateField()
    proposed_end_date = models.DateField()
    acn_number =  models.CharField(max_length=100, null=True, blank=True)
    alead_agency = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='acns')
    alead_co_agency = models.ManyToManyField(Portfolio,  blank=True, related_name='aco_leads')
    final_report_due_date = models.DateField(null=True, blank=True)
    program_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='aprogram_lead')
    technical_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='atechnical_lead')
    finance_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='afinance_lead')
    description = models.TextField(null=True, blank=True)
    aworeda = models.ManyToManyField(ImplementationArea,  blank=True, related_name='activity_woredas')
    
    mc_budget = models.FloatField(null=True, blank=True)
    
    cost_sharing_budget = models.FloatField(null=True, blank=True)
    USD = 1
    ETB = 2
    CURRENCY_CHOICES =   (
        (USD, 'USD'),
        (ETB, 'ETB'),
     
        )

 
    mc_currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
    cs_currency =  models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
    
    
   

    STATUS_CHOICES = [(False, 'Draft'), (True, 'Submitted')]
    status = models.BooleanField("Status", default=False, 
                                       choices=STATUS_CHOICES)
    approval_status = models.CharField(max_length=100,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self,*args, **kwargs):
        suffix = f"{self.pk}".zfill(4)
        self.acn_number = f"{self.icn.icn_number}/ACN/{suffix}"
        super(Activity, self).save(*args, **kwargs)

    def get_num_impact(self):
        if ActivityImpact.objects.filter(activity_id=self).exists():
            qs = ActivityImpact.objects.filter(activity_id=self).annotate(Count('impact', distinct=True))
            num = qs[0].impact__count
        else:
            num = 0
        return num
    
    def get_name(self):
        return "Activity"
        
       
    def __str__(self):
        return self.title

class ActivityImplementationArea(models.Model):
    activity =  models.ForeignKey(
        Activity, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        NRegion, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(
        NZone, on_delete=models.CASCADE, null=True, blank=True)
    woreda = models.OneToOneField(NWoreda, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
    
class ActivityImpact(models.Model):
    activity =  models.ForeignKey(
        Activity, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    impact_pilot  = models.IntegerField(null=True, blank=True)
    impact_scaleup  = models.IntegerField(null=True, blank=True)
    impact = models.ManyToManyField(Impact, related_name='activityimpacts')

    def __str__(self):
        return str(self.pk)

class ActivityDocument(models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='auploaded_by')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,  blank=True)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(null=True,  blank=True, max_length=500, upload_to=path_and_rename)
    ver = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)

    class Meta:
        ordering = ('-uploaded_at',)
    
    def __str__(self):
        return "%s %s %s" % ("Version", self.ver, self.user.email.split('@')[0])

class ActivitySubmit(models.Model):
    Draft = 1
    Submit = 2
    
    SSTATUS = (
        (Draft, 'Draft'),
        (Submit, 'Request Submitted'),
     
        )
    id = models.AutoField(primary_key=True)
    activity =  models.ForeignKey(
        Activity, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    submission_status = models.ForeignKey(Submission_Status, on_delete=models.CASCADE)
    submission_note = models.TextField(null=True,  blank=True)

    document = models.ForeignKey(ActivityDocument, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ('-submission_date',)
    
    
    def save(self, *args, **kwargs):
        if self.submission_date and self.old_submission_date != self.submission_date:
            self.submission_date = timezone.now()
        super(ActivitySubmit, self).save(*args, **kwargs)
   
    
    def __str__(self):
        return str(self.id)

class ActivitySubmitApproval_T(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Approved'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivitySubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivitySubmitApproval_T, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivitySubmitApproval_T, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)

class ActivitySubmitApproval_P(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Approved'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivitySubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivitySubmitApproval_P, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivitySubmitApproval_P, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)

class ActivitySubmitApproval_F(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Approved'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivitySubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivitySubmitApproval_F, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivitySubmitApproval_F, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)
    



    
    
    
