from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRedirect
from django_htmx.http import HttpResponseClientRefresh
# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from .forms import TravelRequestForm, TravelCostForm, FinanceCodeForm, RequestSubmitForm, RequestCancelForm, ApprovalForm_B, ApprovalForm_F, ApprovalForm_S
from .models import Travel_Request, Estimated_Cost, Finance_Code,RequestSubmit, SubmitApproval_B, SubmitApproval_F, SubmitApproval_S
from program.models import TravelUserRoles, Program
from app_admin.models import Submission_Status, Approvalf_Status
from user.models import Profile
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives



@login_required(login_url='login') 
def travel(request):
    trequests = Travel_Request.objects.all()
    context = {'trequests':trequests}
   
 
    # add the dictionary during initialization
  
   

    return render(request, 'travel_step.html', context)

@login_required(login_url='login') 
def trequest_detail(request, id):
    trequests = Travel_Request.objects.all()
   
    trequest = Travel_Request.objects.get(pk=id)
    context = {'trequests':trequests,'trequest':trequest}
    print(trequest.id)
    
    return render(request, 'travel_step_profile_detail.html', context)


@login_required(login_url='login') 
def trequest_new(request):
    trequests = Travel_Request.objects.all()
    form = TravelRequestForm()
    if request.method == 'POST':
        form = TravelRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
           
            return redirect('trequest_detail',instance.pk) 
        
    context = {'trequests':trequests,'form':form}
    return render(request, 'travel_step_profile_new.html', context)
    
@login_required(login_url='login') 
def trequest_edit(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    trequests = Travel_Request.objects.all()
    form = TravelRequestForm()

    if request.method == "POST":
       
        form = TravelRequestForm(request.POST, instance=trequest)
        if form.is_valid():
            instance = form.save()

            return redirect('trequest_detail',instance.pk) 
            
          

    form = TravelRequestForm(instance=trequest) 
    context = {'form':form, 'trequests':trequests,'trequest':trequest}
    return render(request, 'travel_step_profile_new.html', context)




@login_required(login_url='login') 
def trequest_cost(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    trequests = Travel_Request.objects.all()
    if Estimated_Cost.objects.filter(travel_request_id=trequest.id).exists():
        travel_cost = Estimated_Cost.objects.filter(travel_request_id=trequest.id)
        total_cost = sum(travel_cost.values_list('total_cost', flat=True))
   
        context = {'trequest':trequest, 'total_cost':total_cost, 'trequests':trequests}
    else:
        context = {'trequest':trequest, 'trequests':trequests}
    
    return render(request, 'travel_step_profile_cost.html', context)

@login_required(login_url='login') 
def add_travel_cost(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    form = TravelCostForm(trequest=trequest)
    if request.method == 'POST':
        form = TravelCostForm(request.POST, trequest=trequest)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.travel_request = trequest
            instance.save()
            trequest = Travel_Request.objects.get(id=instance.travel_request_id)
            if Estimated_Cost.objects.filter(travel_request_id=trequest.id).count() == 2 or Estimated_Cost.objects.filter(travel_request_id=trequest.id).count() < 2:
                return HttpResponseClientRedirect('/travel/request/'+str(trequest.id)+'/cost/')
            else:
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "CostChanged": None,
                            "showMessage": f"{instance.id} added."
                        })
                    })         
       
    context = {'form':form, 'trequest':trequest}
    return render(request, 'partial/add_cost.html', context)

@login_required(login_url='login') 
def travel_cost_detail(request, id):
    travel_cost = Estimated_Cost.objects.get(pk=id)
    context = {'travel_cost':travel_cost}
   
    
    return render(request, 'partial/cost_detail.html', context)

@login_required(login_url='login') 
def edit_travel_cost(request, id):
    travel_cost = Estimated_Cost.objects.get(pk=id)
    if request.method == "POST":
        form = TravelCostForm(request.POST, instance=travel_cost)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "CostChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })          
          

    form = TravelCostForm(instance=travel_cost) 
    context = {'form':form, 'travel_cost':travel_cost}
    return render(request, 'partial/edit_cost.html', context)

@login_required(login_url='login') 
def delete_travel_cost(request, id):
    travel_cost = Estimated_Cost.objects.get(pk=id)
    travel_cost.delete()
    return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "CostChanged": None,
                        "showMessage": f"{travel_cost.id} deleted."
                    })
                })    


@login_required(login_url='login') 
def add_finance_code(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    form = FinanceCodeForm()
    if request.method == 'POST':
        form = FinanceCodeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.travel_request = trequest
            instance.save()
            trequest = Travel_Request.objects.get(id=instance.travel_request_id)
            print(trequest.get_finance_total())
            if trequest.get_finance_total() == 100.00 :
                return HttpResponseClientRedirect('/travel/request/'+str(trequest.id)+'/cost/')
            else:
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "FinanceChanged": None,
                            "showMessage": f"{instance.id} added."
                        })
                    })

            
           
            
       
    context = {'form':form, 'trequest':trequest}
    return render(request, 'partial/add_finance_code.html', context)

@login_required(login_url='login') 
def finance_code_detail(request, id):
    finance_code = Finance_Code.objects.get(pk=id)
    context = {'finance_code':finance_code}
   
    
    return render(request, 'partial/finance_code_detail.html', context)

def edit_finance_code(request, id):
    finance_code = Finance_Code.objects.get(pk=id)
    if request.method == "POST":
        form = FinanceCodeForm(request.POST, instance=finance_code)
        if form.is_valid():
            instance = form.save()

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FinanceChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
            
          

    form = FinanceCodeForm(instance=finance_code) 
    context = {'form':form, 'finance_code':finance_code}
    return render(request, 'partial/edit_finance_code.html', context)



@login_required(login_url='login') 
def delete_finance_code(request, id):
    finance_code = Finance_Code.objects.get(pk=id)
    finance_code.delete()
    return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FinanceChanged": None,
                        "showMessage": f"{finance_code.id} added."
                    })
                })


@login_required(login_url='login') 
def cost_list(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    travel_cost = Estimated_Cost.objects.filter(travel_request_id=trequest.id)
    total_cost = sum(travel_cost.values_list('total_cost', flat=True))
    
    context = {'travel_cost':travel_cost, 'trequest':trequest, 'total_cost':total_cost}
   
    
    return render(request, 'partial/cost_list.html', context)

def lincodes(request):
    form = FinanceCodeForm(request.GET)
    return HttpResponse(form['lin_code'])


@login_required(login_url='login') 
def finance_list(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    finance_code = Finance_Code.objects.filter(travel_request_id=trequest.id)
    total_code = sum(finance_code.values_list('value', flat=True))
    
    context = {'finance_code':finance_code, 'trequest':trequest, 'total_code':total_code}
   
    
    return render(request, 'partial/finance_list.html', context)


@login_required(login_url='login') 
def trequest_review(request, id):
    trequests = Travel_Request.objects.all()
    trequest = Travel_Request.objects.get(pk=id)
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    program = Program.objects.get(travel_users_role=profile)
    form = RequestSubmitForm(user=user)
   
    context = {'trequests':trequests,'trequest':trequest, 'form':form}
    
    return render(request, 'travel_step_profile_review.html', context)

@login_required(login_url='login') 
def trequest_approval(request, id):
    trequests = Travel_Request.objects.all()
    trequest = Travel_Request.objects.get(pk=id)
    context = {'trequests':trequests,'trequest':trequest}
    
    return render(request, 'travel_step_profile_approval.html', context)

@login_required(login_url='login') 
def submit_request(request, id, sid):
    trequest = Travel_Request.objects.get(pk=id)
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    program = Program.objects.get(travel_users_role=profile)
    form = RequestSubmitForm(user=user, sid=sid)
    if request.method == 'POST':
        form = RequestSubmitForm(request.POST, user=user, sid=sid)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.travel_request = trequest
            instance.save()
            requestsubmit = get_object_or_404(RequestSubmit, pk=instance.pk)
            #Document.objects.create(user = icn.user, document = instance.document,  icn=instance.icn, description = document_i)
          
            if requestsubmit.status_id == 2:
                
                
                SubmitApproval_B.objects.create(user = requestsubmit.budget_holder,submitrequest_id = instance.id, approval_status=Approvalf_Status.objects.get(id=1))
                SubmitApproval_F.objects.create(user = requestsubmit.finance_reviewer,submitrequest_id = instance.id, approval_status=Approvalf_Status.objects.get(id=1))
                SubmitApproval_S.objects.create(user = requestsubmit.security_reviewer,submitrequest_id = instance.id, approval_status=Approvalf_Status.objects.get(id=1))
               
                send_notify(requestsubmit.id)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "RequestChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })

    context = {'trequest':trequest, 'form':form}
    return render(request, 'partial/submit.html', context)


@login_required(login_url='login') 
def edit_request(request, id, sid):
    trequest = Travel_Request.objects.get(pk=id)
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    program = Program.objects.get(travel_users_role=profile)
    requestsubmit = get_object_or_404(RequestSubmit, travel_request_id = trequest.id)
    form = RequestCancelForm(instance= requestsubmit, user=user, sid=sid)
    if request.method == 'POST':
        form = RequestCancelForm(request.POST,instance= requestsubmit, user=user, sid=sid)
        if form.is_valid():
            instance = form.save()
            
            requestsubmit = get_object_or_404(RequestSubmit, pk=instance.pk)
            #Document.objects.create(user = icn.user, document = instance.document,  icn=instance.icn, description = document_i)
          
            if requestsubmit.status_id == 1:
                submitapproval_b = SubmitApproval_B.objects.get(submitrequest_id=requestsubmit.id)
                submitapproval_b.delete()
                submitapproval_f = SubmitApproval_F.objects.get(submitrequest_id=requestsubmit.id)
                submitapproval_f.delete()
                submitapproval_s = SubmitApproval_S.objects.get(submitrequest_id=requestsubmit.id)
                submitapproval_s.delete()

            elif requestsubmit.status_id == 2:
                SubmitApproval_B.objects.create(user = requestsubmit.budget_holder,submitrequest_id = instance.id, approval_status=Approvalf_Status.objects.get(id=1))
                SubmitApproval_F.objects.create(user = requestsubmit.finance_reviewer,submitrequest_id = instance.id, approval_status=Approvalf_Status.objects.get(id=1))
                SubmitApproval_S.objects.create(user = requestsubmit.security_reviewer,submitrequest_id = instance.id, approval_status=Approvalf_Status.objects.get(id=1))
               
                send_notify(requestsubmit.id)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "RequestChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })

    context = {'trequest':trequest, 'form':form}
    return render(request, 'partial/submit.html', context)

@login_required(login_url='login') 
def submit_approval_list(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    context = {'trequest':trequest}
    return render(request, 'partial/submit_approval.html', context)
    
@login_required(login_url='login') 
def approval_list(request, id):
    trequest = Travel_Request.objects.get(pk=id)
    context = {'trequest':trequest}
    return render(request, 'partial/approval.html', context)


@login_required(login_url='login') 
def approve_requestb(request, id, aid):
    submitapprovalb = SubmitApproval_B.objects.get(pk=id)
    form = ApprovalForm_B(instance= submitapprovalb,  aid=aid)
    if request.method == 'POST':
        form = ApprovalForm_B(request.POST,instance= submitapprovalb, aid=aid)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ApprovalChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })

    context = { 'form':form}

    return render(request, 'partial/approval_formb.html', context)

@login_required(login_url='login') 
def approve_requestf(request, id, aid):
    submitapprovalf = SubmitApproval_F.objects.get(pk=id)
    form = ApprovalForm_F(instance= submitapprovalf,  aid=aid)
    if request.method == 'POST':
        form = ApprovalForm_F(request.POST,instance= submitapprovalf, aid=aid)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ApprovalChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })

    context = { 'form':form}

    return render(request, 'partial/approval_formf.html', context)

@login_required(login_url='login') 
def approve_requests(request, id, aid):
    submitapprovals = SubmitApproval_S.objects.get(pk=id)
    print(submitapprovals)
    form = ApprovalForm_S(instance= submitapprovals,  aid=aid)
    if request.method == 'POST':
        form = ApprovalForm_S(request.POST,instance= submitapprovals, aid=aid)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ApprovalChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })

    context = { 'form':form}

    return render(request, 'partial/approval_forms.html', context)


def send_notify(id):
    requstsubmit = get_object_or_404(RequestSubmit, id=id)
    if requstsubmit.status_id == 2:
        subject = 'Request for Travel Approval'
        initiator = requstsubmit.travel_request.user.profile.full_name
        user_role = 'Initiator'
    elif requstsubmit.status_id == 1:
        subject = 'Travel Request temporarily withdrawn'
        initiator = requstsubmit.travel_request.user.profile.full_name
        user_role = 'Initiator'
        
  
        

    subject = subject
    context = {
                "program": requstsubmit.travel_request.user.profile,
                "title": requstsubmit.travel_request.purpose,
                "id": requstsubmit.id,
                
                "creator": requstsubmit.travel_request.user.profile,
                "initiator": initiator,
                "user_role": user_role,
            
                
                }
    html_message = render_to_string("partial/intervention_mail.html", context=context)
    plain_message = strip_tags(html_message)
    recipient_list = [requstsubmit.budget_holder.profile.user.email, requstsubmit.finance_reviewer.profile.user.email, requstsubmit.security_reviewer.profile.user.email,requstsubmit.travel_request.user.email]
        
    message = EmailMultiAlternatives(
        subject = subject, 
        body = plain_message,
        from_email = None ,
        to= recipient_list
            )
        
    message.attach_alternative(html_message, "text/html")
    message.send()


