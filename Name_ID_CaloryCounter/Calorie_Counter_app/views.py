from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

from datetime import date
from django.db.models import Sum,Count
from django.contrib.auth.forms import AuthenticationForm

from Calorie_Counter_app.models import*
from Calorie_Counter_app.forms import *


## registration page ##


def register_page(request):
    if request.method=='POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'registration complete')
            return redirect('login_page')
    else:
        form_data=RegistrationForm()
    context={
        'form_data' : form_data,
        'form_title' : 'Registration Form',
        'form_btn' : 'save'
    }
    return render(request,'master/base-form.html',context)




###login page####

def login_page(request):
    form_data = AuthenticationForm(request, data=request.POST)
    if request.method=='POST':
        if form_data.is_valid():
            user=form_data.get_user()
            login(request,user)
            return redirect('dashboard_page')
    context={
        'form_data' : form_data,
        'form_title' : "LOGIN FORM",
        'form_btn' : 'save'
    }
    return render(request,'master/base-form.html',context)




###logout page###


@login_required
def logout_page(request):
    logout(request)
    messages.success(request,'logout success')
    return redirect('login_page')




### profile create edit delete page ###


@login_required
def profile_page(request):
    profile=InfoModel.objects.filter(
        user=request.user).first()
    if request.method=='POST':
        form_data = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        
        if form_data.is_valid():
            save_data = form_data.save(commit=False)
            save_data.user=request.user
            weight = save_data.weight
            height = save_data.height
            age = save_data.age 
            if save_data.gender=='male':
                bmr_calculate = 66.47 +(13.75*weight)+(5.003*height)-(6.755*age)
            else:
                bmr_calculate = 655.1 +(9.563*weight)+(1.850*height)-(4.676*age)
                
            save_data.bmr = bmr_calculate
            save_data.save()
            if profile:
                messages.success(request,
                'Profile updated successfully')
            else:
                messages.success(request,
                'Profile Created Successfully')
            return redirect('profile_page')
    
    if request.method=='POST' and 'delete_profile' in request.POST:
        if profile:
            profile.delete()
            messages.success(request,'Profile Deleted Successfully')
        return redirect('profile_page')

    else:
        form_data = ProfileForm(instance=profile)

    if not profile or request.GET.get('edit'):
        context={
        'form_data' : form_data,
        'form-title' : 'profile form',
        'form_btn' : 'Save profile'
    }
        return render(request,'master/base-form.html', context)

    return render(request,'profile.html',{'profile' : profile})




##  calorie List ##


def calorie_list(request):
    consumed_data = ConsumedCalModel.objects.filter(consumed_by=request.user)
    return render(request,'calorie_list.html',{'consumed_data' : consumed_data})




##All  in one calorie###


@login_required
def calorie_page(request):

    calorie_id = request.GET.get('id')

    data = ConsumedCalModel.objects.filter(
        id=calorie_id,
        consumed_by=request.user
    ).first()

    if request.method == 'POST' and 'delete_calorie' in request.POST:
        if data:
            data.delete()
            messages.success(
                request,
                'Calorie Deleted Successfully'
            )
        return redirect('calorie_list')

    elif request.method == 'POST':
        form_data = CaloriesForm(
            request.POST,
            instance=data
        )

        if form_data.is_valid():
            save_data = form_data.save(commit=False)
            save_data.consumed_by = request.user
            save_data.save()

            if data:
                messages.success(
                    request,
                    'Calorie Updated Successfully'
                )
            else:
                messages.success(
                    request,
                    'Calorie Created Successfully'
                )

            return redirect('calorie_list')

    else:
        form_data = CaloriesForm(instance=data)

    if not data or request.GET.get('edit'):
        context = {
            'form_data': form_data,
            'form_title': 'calorie form',
            'form_btn': 'Save calorie'
        }
        return render(
            request,
            'master/base-form.html',
            context
        )

    return render(
        request,
        'calorie.html',
        {'data': data}
    )


###DASHBOARD PAGE###


@login_required
def dashboard_page(request):
    current_user = request.user

    try:
        bmr = round(request.user.user_info.bmr,2)
    except:
        bmr = 0

    today = date.today()

    today_consumed_data = ConsumedCalModel.objects.filter(
        consumed_by=current_user,
        created_by__date=today
    )

    total_consumed_calories = today_consumed_data.aggregate(
        total_calorie=Sum('calorie'),
        total_count=Count('calorie')
    )

    total_caloire = total_consumed_calories['total_calorie'] or 0

    less_more = bmr-total_caloire

    if round(bmr) > round(total_caloire):
        suggestion = "beshi kha calorie kom."
    elif round(bmr) == round(total_caloire):
        suggestion = "calorie to thikthak ase re."
    else:
        suggestion = "kom kha calorie beshi."

    context = {
        'required_calories': bmr,
        'today_consumed_data': today_consumed_data,
        'consumed_calories': total_caloire,
        'total_count': total_consumed_calories['total_count'],
        'less_more': less_more,
        'suggestion': suggestion,
    }

    return render(request,'dashboard.html',context)
    