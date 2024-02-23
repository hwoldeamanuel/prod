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




 

register = template.Library()
import datetime




def jsonify(data):
    if isinstance(data, dict):
        return data
    else:
        return json.loads(data)
  

def account(request):
    user_activity = CRUDEvent.objects.filter(user=request.user).order_by('-id')[:12]
     

    for item in  user_activity:
      item.object_json_repr = jsonify(item.object_json_repr)
    qs1 = RequestEvent.objects.filter(user_id=request.user).values('datetime__date').annotate(id_count=Count('id', distinct=True))
    qs2 = RequestEvent.objects.filter(user_id=request.user, method='POST').values('datetime__date').annotate(count_login=Count('id', distinct=True))
  




    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['datetime__date']].update(collectible.items())

    all_request = list(collector.values()) 

  
    
    context = {'user_activity':user_activity, 'all_request':all_request}
    return render(request, 'accounts.html', context)

@register.filter(name='jsonify')
def jsonify(data):
    if isinstance(data, dict):
        return data
    else:
        return json.loads(data)

  
def user_activity(request):
    qs1 = RequestEvent.objects.filter(user_id=request.user).values('datetime__date').annotate(id_count=Count('id', distinct=True))
    qs2 = RequestEvent.objects.filter(user_id=request.user, method='POST').values('datetime__date').annotate(count_login=Count('id', distinct=True))
  




    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['datetime__date']].update(collectible.items())

    all_request = list(collector.values())

    context = {'all_request':all_request,}
    return render(request, 'partial/user_activity.html', context)



     

  
def activity_filter(request):
    query = request.GET.get('dates', '')
    print(query)
    print("hye")
    
    return render(request, 'partial/admin_boundary.html')

  
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('account')
    



# Create your views here.
  
def userprofile(request):
    user = request.user
    user = User.objects.get(pk=user.id)
    context = {'user': user}
    return render(request, 'registration/user_profile.html', context)

  
def add_profile(request, id): 
    user = User.objects.get(pk=id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserprofileChanged": None,
                        "showMessage": f"{user.email} updated."
                    })
                })
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profile_form.html', {
        'form': form,
    })


  
def user_profile(request): 
   
    user = User.objects.get(pk=request.user.id)
    context = {'user': user}
    return render(request, 'partial/user_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change_form.html', {
        'form': form
    })
def change_success(request):
    return render(request, 'partial/password_change_success.html')

def home(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.count
  #total_icn = Icn.objects.count
  #total_activity = Activity.objects.count
  program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
  total_woreda = ImplementationArea.objects.count
  context = {'program_users':program_users,'total_program': total_program, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda}
  return render(request, 'dashboard_main.html', context)

def home_chart(request):

    # get the year from GET request, or default to the maximum year in the data
    
    program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]

    context = {'program_users':program_users,}
    
    return render(request, 'dashboard.html', context)


def dashboard(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.count
 # total_icn = Icn.objects.count
  #total_activity = Activity.objects.count
  program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
  total_woreda = ImplementationArea.objects.count
  context = {'program_users':program_users,'total_program': total_program, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda}
  return render(request, 'dashboard2 copy.html', context)