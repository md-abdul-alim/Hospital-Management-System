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

from doctor.models import *
from patient.models import *
from hospital.models import *
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

#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor/doctor_dashboard.html',context=mydict)



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor/doctor_patient.html',context=mydict)



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='login')
# @user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
