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
from .models import *
from hospital.validators import redirectlogin
# Create your views here.

#---------------------Patient registration------------------------------

def patient_registration(request):
    user = request.user
    if user.is_authenticated:
        return redirectlogin(request)
    else:
        userForm=CreateUserForm()
        patientForm=PatientForm()
        context={
            'userForm':userForm,
            'patientForm':patientForm
        }
        if request.method=='POST':
            print("post")
            userForm=CreateUserForm(request.POST or None)
            patientForm=PatientForm(request.POST,request.FILES or None)
            if userForm.is_valid() and patientForm.is_valid():
                userForm=userForm.save()
                #userForm.set_password(user.password)
                group = Group.objects.get(name='PATIENT')
                userForm.groups.add(group)

                patientForm=patientForm.save(commit=False)
                patientForm.user=userForm
                patientForm.assignedDoctorId=request.POST.get('assignedDoctorId')
                patientForm.save()
                print("valid")
                return redirect('login')
            else:
                print("Post not valid")
                context={
                    'userForm':userForm,
                    'patientForm':patientForm
                }
                return render(request,'hospital/registration/patientsignup.html',context)
        else:
            return render(request,'hospital/registration/patientsignup.html',context)
