from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import QueryDict
# Create your views here.
from django.contrib.auth.decorators import login_required
from portfolio.models import Portfolio
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import ProgramForm, AddProgramAreaForm, IndicatorForm, UserRoleForm, UserRoleFormE, UserForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Program, ImplementationArea, Indicator, UserRoles
from django.contrib.auth.models import User
from conceptnote.models import Icn, Activity
from django.db.models.functions import TruncMonth
from django.db.models import Q
from collections import defaultdict
from itertools import chain
from report.models import IcnReport, ActivityReport
from django.contrib.auth.decorators import permission_required

@login_required(login_url='login')
def program(request):
    user = request.user
    if user.is_superuser:
        programs = Program.objects.all().order_by('-id')
    elif Program.objects.filter(users_role=user).count() == 1:
        program = Program.objects.get(users_role=user)
        return redirect('program_detail',pk=program.id) 
    
    else:
        programs =  program = Program.objects.filter(users_role=user)
    
   
    context = {'programs': programs}
    return render(request, 'programs.html', context)

@login_required(login_url='login')
def program_profile(request, id):
    program = Program.objects.get(pk=id)
    context = {'program': program}
    return render(request, 'partial/program_profile.html', context)

@login_required(login_url='login')
@permission_required("program.can_add_program", raise_exception=True)
def create_view(request): 
    # dictionary for initial data with  
    # field names as keys 
    form = ProgramForm()
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
           
            return redirect('program_detail',instance.pk) 
        
    context = {'form':form}
    return render(request, 'add_program.html', context)


@login_required(login_url='login')
def program_detail(request, pk):
    program = Program.objects.filter(pk=pk)
    qs1 = Icn.objects.filter(program_id = pk).annotate(m=TruncMonth('created')).values("m").annotate(icn_count=Count('id', distinct=True))
    qs2 = Activity.objects.filter(icn__program_id = pk).annotate(m=TruncMonth('created')).values("m").annotate(activity_count=Count('id', distinct=True))
 
    total_icn  =  Icn.objects.filter(program_id = pk).count
    total_acn  =  Activity.objects.filter(icn__program_id = pk).count
    total_report = IcnReport.objects.filter(Q(activityreport__activity__icn__program__in=program), Q(icn__program__in=program)).count 
   
   
    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['m']].update(collectible.items())

    all_request = list(collector.values())
   
    qsi = Icn.objects.filter(program_id = pk).only("title", "id","user","program_lead","technical_lead","finance_lead","status","approval_status","created").order_by("-created")
    qsa = Activity.objects.filter(icn__program_id = pk).only("title", "id", "user","program_lead","technical_lead","finance_lead","status","approval_status","created").order_by("-created")
      
       
    conceptnotes = sorted(list(chain(qsi, qsa)), key=lambda instance: instance.created, reverse=True)
    
    

   
 
    # add the dictionary during initialization
  
    program = Program.objects.get(pk=pk)
    
    context = {'program':program, 'all_request':all_request, 'total_report':total_report,  'total_icn':total_icn, 'total_acn':total_acn, 'conceptnotes': conceptnotes  }
    return render(request, 'program.html', context)

@login_required(login_url='login')
@permission_required("program.can_change_program", raise_exception=True)
def edit_view(request, id): 
    # dictionary for initial data with  
    # field names as keys 
    program = Program.objects.get(pk=id)
    form = ProgramForm()

    if request.method == "POST":
       
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            instance = form.save()

            return redirect('program_detail',instance.pk) 
            
          

    form = ProgramForm(instance=program) 
    context = {'form':form}
    return render(request, 'add_program.html', context)


def edit_program_profile(request, id):
    program = Program.objects.get(pk=id)
    if request.method == "POST":
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            instance =form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ProgramListChanged": None,
                        "showMessage": f"{instance.title} updated."
                    })
                }
            )
        else:
            form = ProgramForm(instance=program)
            return render(request, 'partial/program_profile_form.html', {
            'form': form,
            'program': program,
        })
    form = ProgramForm(instance=program)
    return render(request, 'partial/program_profile_form.html', {
            'form': form,
            'program': program,
        })

         
def search_results_view(request):
    query = request.GET.get('search', '')
   

    all_programs= Program.objects.all().order_by('-id')
    if query:
        qs1 = Program.objects.filter(title__icontains=query)
        qs2 = Program.objects.distinct().filter(portfolio__title__icontains=query)
        
        
        programs = qs1.union(qs2).order_by('id')
       
    else:
        programs = Program.objects.all().order_by('-id')

    context = {'programs': programs, 'count': all_programs.count()}
    return render(request, 'partial/program_list.html', context)  

   
 

def area_update(request, pk):
    area = get_object_or_404(ImplementationArea, pk=pk)
    program = area.program_id
    regions = Region.objects.all()
    context = {'area': area, 'regions':regions }
    if request.method == "PUT":
        data = QueryDict(request.body).dict()
        form = AddProgramAreaForm(data, instance=area)
        if form.is_valid():
            form.save()      
            areas =ImplementationArea.objects.filter(program_id=program).order_by('region_id','zone_id','woreda_id')
            context = {'areas': areas, 'regions':regions }
            return render(request, 'area_list.html', context)

        context['form'] = form
        return render(request, 'area_form_edit.html', context)



def region(request, id):
    program = get_object_or_404(Program, pk=id)
    if request.method == "POST":
        form = AddProgramAreaForm(request.POST or none)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.program = Program.objects.get(pk=id)
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "areaListChanged": None,
                        "showMessage": f"{instance.woreda} added."
                    })
                })
    
    form = AddProgramAreaForm()
    context = {'form': form}
    
    return render(request, 'partial/area_form.html', context)

def zones(request):
    form = AddProgramAreaForm(request.GET)
    return HttpResponse(form['zone'])


   

def woredas(request):
    form = AddProgramAreaForm(request.GET)
    return HttpResponse(form['woreda'])

def area_edit_form(request, pk):
    area = get_object_or_404(ImplementationArea, pk=pk)    
    if request.method == "GET":
        iarea = get_object_or_404(ImplementationArea, pk=int(pk))
        form = AddProgramAreaForm(instance=iarea)
        context = {'area': area, 'form': form }
        return render(request, 'partial/area_form_edit.html', context)

    elif request.method == "PUT":
        area = get_object_or_404(ImplementationArea, pk=int(pk))
        data = QueryDict(request.body).dict()
        form = AddProgramAreaForm(data, instance=area)
        if form.is_valid():
            instance=form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "areaListChanged": None,
                        "showMessage": f"{instance.woreda} updated."
                    })
                }
            )
     
       




def edit_user_role(request, uid):
   
    user = User.objects.get(pk=uid)
   
    
   
        
    if request.method == "PUT":
        user = User.objects.get(pk=uid)
        data = QueryDict(request.body).dict()
        form = UserRoleFormE(data, instance=user, user=user)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.username} updated."
                    })
                })
        
        form = UserRoleFormE(instance=user, user=user) 
        context = {'form': form}
        return render(request, 'partial/edit_user_role.html', context)
    
    form = UserRoleFormE(instance=user, user=user) 
    context = {'form':form}
    return render(request, 'partial/edit_user_role.html', context)



def delete_program(request, pk):
    program = get_object_or_404(Program, pk=pk)
   
    program.delete()
    programs =programs.objects.all()
    return render(request, 'programs.html', {'programs': programs})
    
def indicator_list(request, id):
    return render(request, 'partial/indicator_list.html', {
        'indicators': Indicator.objects.filter(program_id=id),
    })


def add_indicator(request, id):
    if request.method == "POST":
        form = IndicatorForm(request.POST)
        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.program = get_object_or_404(Program, pk=id)
            indicator.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "IndicatorListChanged": None,
                        "showMessage": f"{indicator.indicator_title} added."
                    })
                })
    else:
        form = IndicatorForm()
    return render(request, 'partial/indicator_form.html', {
        'form': form,
    })


def edit_indicator(request, pk):
    indicator = get_object_or_404(Indicator, pk=pk)
    if request.method == "POST":
        form = IndicatorForm(request.POST, instance=indicator)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "IndicatorListChanged": None,
                        "showMessage": f"{indicator.indicator_title} updated."
                    })
                }
            )
    else:
        form = IndicatorForm(instance=indicator)
    return render(request, 'partial/indicator_form.html', {
        'form': form,
        'indicator': indicator,
    })



def remove_indicator(request, pk):
    indicator = get_object_or_404(Indicator, pk=pk)
    indicator.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "IndicatorListChanged": None,
                "showMessage": f"{indicator.indicator_title} deleted."
            })
        })

def user_list(request, id):
    program = get_object_or_404(Program, pk=id)
    program_users = UserRoles.objects.filter(program=program)
    return render(request, 'partial/user_list_program.html', {
        'users': program_users,
    })

def add_user(request, id):
    program = Program.objects.get(pk=id)
    if request.method == "POST":
        program = Program.objects.get(pk=id)
        form = UserRoleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.program = program
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.user} updated."
                    })
                })
    else:
        form = UserRoleForm(program=program)
    return render(request, 'partial/user_role.html', {
        'form': form,
        
    })

def area_list(request, id):
    return render(request, 'partial/area_list.html', {
        'areas': ImplementationArea.objects.filter(program_id=id),
    })


def update_user_roles(request, id):
    
    user_role = UserRoles.objects.get(pk=id)
    user = get_object_or_404(User, pk=id)
    if request.method == "PUT":
        user_role = UserRoles.objects.get(pk=id)
        data = QueryDict(request.body).dict()
        form = UserRoleFormE(data, instance=user_role, user=user)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.user } updated."
                    })
                })
        
        form = UserRoleFormE(instance=user_role, user=user) 
        context = {'form': form}
        return render(request, 'partial/edit_user_role.html', context)
    
    else:
        form = UserRoleFormE(instance=user_role, user=user)
        return render(request, 'partial/edit_user_role.html', {
        'form': form,
        'user_role': user_role,
    })


def remove_user_role(request, pk):
    user_role = get_object_or_404(UserRoles, pk=pk)
    user_role.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "UserListChanged": None,
                "showMessage": f"{user_role.user} deleted."
            })
        })



def delete_program(request, pk):
    program = Program.objects.get(pk=pk)
    program.delete()
    programs = Program.objects.all().order_by('-id')
    
    return redirect('programs_list')

def delete_area(request, pk):
    area = get_object_or_404(ImplementationArea, pk=pk)
    area.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "areaListChanged": None,
                "showMessage": f"{area.woreda} deleted."
            })
        })

def newportfolio(request):
    portfolio = Portfolio.objects.all()
    form = ProgramForm(portfolio=portfolio)
   
    return HttpResponse(form['portfolio'])

