from django.shortcuts import render

# Create your views here.
from django.db.models import Max, Avg,Sum,Count


from program.models import Program, ImplementationArea
from portfolio.models import Portfolio
from django.contrib.auth.models import User

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



@login_required(login_url='login')
def home(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.count
  #total_icn = Icn.objects.count
  #total_activity = Activity.objects.count
  program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
  total_woreda = ImplementationArea.objects.count
  context = {'program_users':program_users, 'total_program': total_program, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda}
  return render(request, 'home/dashboard_main.html', context)



@login_required(login_url='login')
def dashboard(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.count
 # total_icn = Icn.objects.count
  #total_activity = Activity.objects.count
  
  
  total_woreda = ImplementationArea.objects.count
  context = {'total_program': total_program, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda}
  return render(request, 'home/dashboard2 copy.html', context)

@login_required(login_url='login')
def program_activity(request):
    
    program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
    context = {'program_users':program_users }
    return render(request, 'home/program_activity.html', context)

