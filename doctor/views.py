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
#---------------------Doctor registration------------------------------
# def doctor_registration(request):
#     user = request.user
#     if user.is_authenticated:
#         return redirectlogin(request)
#     else:
#         userForm=forms.CreateUserForm()
#         doctorForm=forms.DoctorForm()
#         context={
#             'userForm':userForm,
#             'doctorForm':doctorForm
#         }
#         print("GET")
#         if request.method=='POST':
#
#             userForm=forms.CreateUserForm(request.POST)
#             doctorForm=forms.DoctorForm(request.POST,request.FILES)
#             print("before POST")
#
#             if userForm.is_valid() and doctorForm.is_valid():
#                 print("POST")
#                 userForm=userForm.save()
#                 # user.set_password(user.password)
#                 # user.save()
#                 print("user saved")
#                 group = Group.objects.get_or_create(name='DOCTOR')
#                 userForm.groups.add(group)
#                 print("Group added")
#                 doctorForm=doctorForm.save(commit=False)    #documentation: https://stackoverflow.com/questions/12848605/django-modelform-what-is-savecommit-false-used-for
#                 print("doctor saved")
#                 doctorForm.user=userForm
#                 print("doctor user saved")
#                 doctorForm=doctorForm.save()
#                 print("All saved")
#                 # my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
#                 # my_doctor_group[0].user_set.add(user)
#                 return redirect('login')
#             else:
#                 return HttpResponse("Error")
#         return render(request,'hospital/registration/doctorsignup.html',context)
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

        print("GET")
        if request.method=='POST':
            userForm=CreateUserForm(request.POST)
            doctorForm=DoctorForm(request.POST,request.FILES)
            print("before POST")
            # userForm.save()
            # print("user saved before post")
            username = request.POST["username"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username already exists.try another one')
                return render(request,'hospital/registration/doctorsignup.html',context)
            else:
                if password1 != password2 :
                    messages.warning(request, 'Password does not match.') #for messages: https://micropyramid.com/blog/basics-of-django-message-framework/
                    return render(request,'hospital/registration/doctorsignup.html',context)
                else:
                    print("Username", username)
                    if userForm.is_valid() and doctorForm.is_valid():
                        print("POST")
                        # username = userForm.cleaned_data['username']
                        # print("username", username)
                        userForm=userForm.save()
                        # user.set_password(user.password)
                        # user.save()
                        print("user saved")
                        group = Group.objects.get(name='DOCTOR')
                        userForm.groups.add(group)
                        print("Group added")
                        doctorForm=doctorForm.save(commit=False)    #documentation: https://stackoverflow.com/questions/12848605/django-modelform-what-is-savecommit-false-used-for
                        print("doctor saved")
                        doctorForm.user=userForm
                        print("doctor user saved")
                        doctorForm=doctorForm.save()
                        print("All saved")
                        # my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                        # my_doctor_group[0].user_set.add(user)
                        return redirect('login')
                    else:
                        return HttpResponse("Error")

        return render(request,'hospital/registration/doctorsignup.html',context)
