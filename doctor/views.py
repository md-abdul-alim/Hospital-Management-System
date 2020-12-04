from django.shortcuts import render,redirect,reverse
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from patient.forms import CreateUserForm
from .models import *
from hospital.validators import redirectlogin

# Create your views here.

def doctor_registration(request):
    user = request.user
    if user.is_authenticated:
        return redirectlogin(request)
    else:
        userForm=CreateUserForm()
        doctorForm=DoctorForm()
        context={
            'userForm':userForm,
            'doctorForm':doctorForm
        }
        if request.method=='POST':
            print("post")
            userForm=CreateUserForm(request.POST or None)
            doctorForm=DoctorForm(request.POST,request.FILES)
            if userForm.is_valid() and doctorForm.is_valid():
                userForm=userForm.save()
                #userForm.set_password(user.password)
                group = Group.objects.get(name='DOCTOR')
                userForm.groups.add(group)

                doctorForm=doctorForm.save(commit=False)
                doctorForm.user=userForm
                doctorForm.save()
                print("valid")
                return redirect('login')
            else:
                print("Post not valid")
                context={
                    'userForm':userForm,
                    'doctorForm':doctorForm
                }
                return render(request,'hospital/registration/doctorsignup.html',context)
        else:
            return render(request,'hospital/registration/doctorsignup.html',context)
