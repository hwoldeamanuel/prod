from django.contrib import admin
from .models import Portfolio_Category, Portfolio_Type, Region, Zone, Woreda, Country, FieldOffice, Approvalt_Status, Approvalf_Status, Submission_Status
# Register your models here.

admin.site.register(Portfolio_Type)
admin.site.register(Portfolio_Category)
admin.site.register(Region)
admin.site.register(Zone)
admin.site.register(Country)
admin.site.register(Woreda)
admin.site.register(FieldOffice)
admin.site.register(Approvalt_Status)
admin.site.register(Approvalf_Status)
admin.site.register(Submission_Status)
