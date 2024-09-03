from django.shortcuts import render

# Create your views here.
from django.db.models import Max, Avg,Sum,Count
from django.db.models import Q

from program.models import Program, ImplementationArea
from portfolio.models import Portfolio
from django.contrib.auth.models import User
from report.models import IcnReport, ActivityReport
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from program.models import Program
import json
from django.db.models import Max, Avg,Sum,Count

from collections import defaultdict
from itertools import chain
from django import template
from easyaudit.models import RequestEvent, CRUDEvent, LoginEvent
from conceptnote.models import Icn, Activity


@login_required(login_url='login')
def home(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.count
  total_icn = Icn.objects.count
  total_activity = Activity.objects.count
  total_cn=0
  program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
  program_cn = Program.objects.annotate(num_cn=Count("icn__activity") + Count("icn")).filter(num_cn__gte=1).order_by('-num_cn')
  
  for program in program_cn:
     total_cn = program.num_cn + total_cn

  total_woreda = ImplementationArea.objects.count
  icn_status =  Icn.objects.values('approval_status').annotate(icn_count=Count('id', distinct=True))
  acn_status = Activity.objects.values('approval_status').annotate(acn_count=Count('id', distinct=True))
  icn_report_status =  IcnReport.objects.values('approval_status').annotate(icn_count=Count('id', distinct=True))
  acn_report_status = ActivityReport.objects.values('approval_status').annotate(acn_count=Count('id', distinct=True))
  
  context = {'program_users':program_users, 'total_program': total_program,'total_cn':total_cn,'program_cn':program_cn, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda, 'total_icn':total_icn, 'total_activity':total_activity,'icn_status':icn_status, 'acn_status':acn_status, 'icn_report_status':icn_report_status, 'acn_report_status':acn_report_status}
  return render(request, 'home/dashboard_main.html', context)



@login_required(login_url='login')
def dashboard(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.count
  total_icn = Icn.objects.count
  total_activity = Activity.objects.count
  
  
  total_woreda = ImplementationArea.objects.count
  context = {'total_program': total_program, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda, 'total_icn':total_icn, 'total_activity':total_activity}
  return render(request, 'home/dashboard2 copy.html', context)

@login_required(login_url='login')
def program_activity(request):
    
    program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
    context = {'program_users':program_users }
    return render(request, 'home/program_activity.html', context)

