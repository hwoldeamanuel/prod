from django.shortcuts import render
from django.http import QueryDict
# Create your views here.
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Country, Region, Zone, Woreda, Portfolio_Type, Portfolio_Category
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from .forms import UserForm, WoredaForm,ZoneForm, TypeForm, CategoryForm, WoredaFormE, GroupForm,RegionForm,UserGroupForm,GroupAddForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserRoleFormE, UserProgramRoleForm, ZoneFormE
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, Count
from easyaudit.models import RequestEvent,LoginEvent
from collections import defaultdict
from itertools import chain
from django.contrib.auth.models import Group, Permission
from program.models import Program,UserRoles


@login_required(login_url='login') 
def user_setting(request):
    users = User.objects.all().order_by('-id')
    context = {'users': users}
    return render(request, 'users_all.html', context)


@login_required(login_url='login')  
def user_group(request, id):
     user = get_object_or_404(User, id=id)
     group = Group.objects.all().order_by('id')
     
     context = {'group':group, 'user':user}

     return render(request, 'partial/user_group.html', context)


@login_required(login_url='login')  
def group_list(request):
     
     groups = Group.objects.all().order_by('id')
     
     context = {'groups':groups,}

     return render(request, 'partial/group_list.html', context)



@login_required(login_url='login') 
def user_group_edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        form = UserGroupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserGroupChanged": None,
                        "showMessage": f"{user.first_name} updated."
                    })
                }
            )
    else:
        form = UserGroupForm(instance=user)
    return render(request, 'partial/user_group_form.html', {
        'form': form,
        'user': user,
    })


@login_required(login_url='login') 
def add_group(request):
    
    form = GroupAddForm()
    if request.method == "POST":
        form = GroupAddForm(request.POST)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "GroupChanged": None,
                         "showMessage": f"{instance.name} added."

                        
                    })
                }
            )
    else:
        form = GroupAddForm()
    return render(request, 'partial/group_add_form.html', {
        'form': form,
    })



@login_required(login_url='login') 
def group_edit(request, id):
    group = get_object_or_404(Group, id=id)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "GroupChanged": None,
                        "showMessage": f"{group.name} updated."
                    })
                }
            )
    else:
        form = GroupForm(instance=group)
    return render(request, 'partial/group_form.html', {
        'form': form,
        'group': group,
    })


@login_required(login_url='login')
def group_setting(request):
    groups = Group.objects.all().order_by('id')
     
    context = {'groups':groups,}

    return render(request, 'group_setting.html', context)


@login_required(login_url='login')   
def group_delete(request, id):
    group = get_object_or_404(Group, pk=id)
   
    group.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "GroupChanged": None,
                "showMessage": f"{group.name} deleted."
            })
        })


@login_required(login_url='login') 
def admin_boundary(request):
    country = Country.objects.all().order_by('-id')
    region = Region.objects.all().order_by('-id')
    zone = Zone.objects.all().order_by('-id')
    woreda_list = Woreda.objects.all().order_by('-id')
    
    page = request.GET.get('page', 1)

    paginator = Paginator(woreda_list, 10)
    try:
        woreda = paginator.page(page)
    except PageNotAnInteger:
        woreda = paginator.page(1)
    except EmptyPage:
        woreda = paginator.page(paginator.num_pages)

  
    context = {'country': country, 'region': region, 'zone': zone, 'woreda':woreda}
    return render(request, 'admin_boundary.html', context)


@login_required(login_url='login') 
def project_type(request):
    type = Portfolio_Type.objects.all().order_by('-id')
    category = Portfolio_Category.objects.all().order_by('-id')
   
    
    context = {'type': type, 'category': category }
    return render(request, 'project_type.html', context)


@login_required(login_url='login')  
def users_list(request):
    users = User.objects.all().order_by('id')
    context = {'users': users}
    return render(request, 'partial/user_list.html', context)


@login_required(login_url='login')
def users_filter(request):
    query = request.GET.get('search', '')
    
    all_users = User.objects.all().order_by('id')
    
    if query:
        users = all_users.filter(email__icontains=query)
       
    else:
        users = all_users

    context = {'users': users}
    return render(request, 'partial/user_list.html', context)


@login_required(login_url='login')
def groups_filter(request):
    query = request.GET.get('search', '')
    
    groups = Group.objects.all().order_by('id')
    
    if query:
        groups = groups.filter(name__icontains=query)
       
    else:
        groups = groups

    context = {'groups': groups}
    return render(request, 'partial/group_list.html', context)



@login_required(login_url='login') 
def edit_user(request, pk):
    user =User.objects.get(pk=pk)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = UserForm(request.POST, request.FILES, instance=user.profile, user=user)

        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserprofileChanged": None,
                        "showMessage": f"{user.email} updated."
                    })
                })
        else:
            user_form = CustomUserChangeForm( instance=user)
            profile_form = UserForm(instance=user.profile, user=user)
            
    else:
       
        user_form = CustomUserChangeForm( instance=user)
        profile_form = UserForm(instance=user.profile, user=user)
    return render(request, 'partial/account_user_form.html', {
        'profile_form':profile_form, 'user_form':user_form
    })


    

  


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'partial/register_form.html'
    

    def form_valid(self, form):
        instance = form.save()  # save the user
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.first_name} added."
                    })
                }
            )
  
  
def admin_list(request):
    
    woreda_list = Woreda.objects.all().order_by('id')
    
    page = request.GET.get('page', 1)

    paginator = Paginator(woreda_list, 50)
    try:
        woreda = paginator.page(page)
    except PageNotAnInteger:
        woreda = paginator.page(1)
    except EmptyPage:
        woreda = paginator.page(paginator.num_pages)

  
    context = {'woreda':woreda}
    return render(request, 'partial/admin_boundary.html', context)

  
def admin_filter(request):
    query = request.GET.get('search', '')
    print(query)
    all_woredas = Woreda.objects.all()
    
    if query:
        qs1 = Woreda.objects.filter(name__icontains=query)
        qs2 = Woreda.objects.distinct().filter(zone__name__icontains=query)
        qs3 = Woreda.objects.distinct().filter(zone__region__name__icontains=query)
        
        woreda_list = qs1.union(qs2, qs3).order_by('id')
        
        
    else:
       woreda_list = all_woredas

        
    page = request.GET.get('page', 1)

    paginator = Paginator(woreda_list, 50)
    try:
        woreda = paginator.page(page)
    except PageNotAnInteger:
        woreda = paginator.page(1)
    except EmptyPage:
        woreda = paginator.page(paginator.num_pages)

    context = {'woreda': woreda}
    return render(request, 'partial/admin_boundary.html', context)

  
def edit_woreda(request, id):
    woreda = get_object_or_404(Woreda, id=id)
    if request.method == "POST":
        form = WoredaFormE(request.POST, instance=woreda)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AdminListChanged": None,
                        "showMessage": f"{woreda.name} updated."
                    })
                }
            )
    else:
        form = WoredaFormE(instance=woreda)
    return render(request, 'partial/woreda_form.html', {
        'form': form,
        'woreda': woreda,
    })


  
def edit_zone(request, id):
    zone = get_object_or_404(Zone, id=id)
    if request.method == "POST":
        form = ZoneFormE(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AdminListChanged": None,
                        "showMessage": f"{zone.name} updated."
                    })
                }
            )
    else:
        form = ZoneFormE(instance=zone)
    return render(request, 'partial/Zone_form.html', {
        'form': form,
        'zone': zone,
    })


  
def add_woreda(request):
    
    form = WoredaForm()
    if request.method == "POST":
        form = WoredaForm(request.POST)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AdminListChanged": None,
                         "showMessage": f"{instance.name} updated."

                        
                    })
                }
            )
    else:
        form = WoredaForm()
    return render(request, 'partial/woreda_form_new.html', {
        'form': form,
    })

  
def add_region(request):
    
    form = RegionForm()
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AdminListChanged": None,
                         "showMessage": f"{instance.name} updated."

                        
                    })
                }
            )
    else:
        form = RegionForm()
    return render(request, 'partial/region_form.html', {
        'form': form,
    })

  
def add_zone(request):
    
    form = ZoneForm()
    if request.method == "POST":
        form = ZoneForm(request.POST)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AdminListChanged": None,
                         "showMessage": f"{instance.name} updated."

                        
                    })
                }
            )
    else:
        form = ZoneForm(request.POST)
        return render(request, 'partial/zone_form_new.html', {
            'form': form,
        })
   
    return render(request, 'partial/zone_form_new.html', {
            'form': form,
        })
  
def type_list(request):
    
    type = Portfolio_Category.objects.all().order_by('id')
    
    context = {'type':type}
    return render(request, 'partial/type_list.html', context)

  
def edit_category(request, id):
    category = get_object_or_404(Portfolio_Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "PortfolioListChanged": None,
                        "showMessage": f"{category.name} updated."
                    })
                }
            )
    else:
        form = CategoryForm(instance=category)
    return render(request, 'partial/category_form.html', {
        'form': form,
        'category': category,
    })


  
def edit_type(request, id):
    type = get_object_or_404(Portfolio_Type, id=id)
    if request.method == "POST":
        form = TypeForm(request.POST, instance=type)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "PortfolioListChanged": None,
                        "showMessage": f"{type.name} updated."
                    })
                }
            )
    else:
        form = TypeForm(instance=type)
        return render(request, 'partial/type_form.html', {
        'form': form,
        'type': type,
    })


  
def add_category(request):
    
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "PortfolioListChanged": None,
                         "showMessage": f"{instance.name} updated."

                        
                    })
                }
            )
    else:
        form = CategoryForm()
    return render(request, 'partial/category_form.html', {
        'form': form,
    })


  
def add_type(request):
    
    form = TypeForm()
    if request.method == "POST":
        form = TypeForm(request.POST)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "PortfolioListChanged": None,
                         "showMessage": f"{instance.name} updated."

                        
                    })
                }
            )
    else:
        form = TypeForm()
    return render(request, 'partial/type_form.html', {
        'form': form,
    })


  
def type_filter(request):
    query = request.GET.get('search', '')
    print(query)
    
    
    if query:
        qs1 = Portfolio_Category.objects.filter(name__icontains=query)
        qs2 = Portfolio_Category.objects.distinct().filter(type__name__icontains=query)
        
        
        type = qs1.union(qs2).order_by('id')
        
    else:
        type = Portfolio_Category.objects.all()

    context = {'type': type}
    return render(request, 'partial/type_list.html', context)

def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    qs1 =RequestEvent.objects.filter(user_id=id).values('datetime__date').annotate(id_count=Count('id', distinct=True))
    qs2 = RequestEvent.objects.filter(user_id=id, method='POST').values('datetime__date').annotate(count_login=Count('id', distinct=True))
  




    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['datetime__date']].update(collectible.items())

    user_activity = list(collector.values())

    context = {'user': user, 'user_activity':user_activity,}
    return render(request, 'user_setting_accounts.html', context)

def user_detail_profile(request, id):
    user = get_object_or_404(User, id=id)
    context = {'user': user}
    return render(request, 'user_setting_profile.html', context)


def user_roles(request, id):
    user = get_object_or_404(User, pk=id)
    program_users = UserRoles.objects.filter(user=user)
    return render(request, 'partial/user_role_program.html', {
        'program_users': program_users,
    })

def update_user_program_roles(request, id):
    
    user_role = UserRoles.objects.get(pk=id)
    program = get_object_or_404(Program,id=user_role.program_id)
    if request.method == "PUT":
        user_role = UserRoles.objects.get(pk=id)
        data = QueryDict(request.body).dict()
        form = UserRoleFormE(data, instance=user_role, program=program)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserProgramListChanged": None,
                        "showMessage": f"{instance.user } updated."
                    })
                })
        
        form = UserRoleFormE(instance=user_role, program=program) 
        context = {'form': form}
        return render(request, 'partial/edit_user_program_role.html', context)
    
    else:
        form = UserRoleFormE(instance=user_role, program=program)
        return render(request, 'partial/edit_user_program_role.html', {
        'form': form,
        'user_role': user_role,
    })

def add_user_program_role(request, id):
    user = User.objects.filter(id=id)
    if request.method == "POST":
        form = UserProgramRoleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = User.objects.get(pk=id)
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserProgramListChanged": None,
                        "showMessage": f"{instance.user} updated."
                    })
                })
    else:
        form = UserProgramRoleForm(user=user)
    return render(request, 'partial/user_program_role.html', {
        'form': form,
        
    })

def remove_user_program_role(request, pk):
    user_role = get_object_or_404(UserRoles, pk=pk)
    user_role.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "UserProgramListChanged": None,
                "showMessage": f"{user_role.user} deleted."
            })
        })