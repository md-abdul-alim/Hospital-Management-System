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
from doctor.models import *
from patient.models import *
from hospital.models import *
from hospital.forms import PatientAppointmentForm
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
                return redirect('login')
            else:
                context={
                    'userForm':userForm,
                    'patientForm':patientForm
                }
                return render(request,'registration/patientsignup.html',context)
        else:
            return render(request,'registration/patientsignup.html',context)

#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='login')
# @user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=Patient.objects.get(user_id=request.user.id)
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'patient/patient_dashboard.html',context=mydict)



@login_required(login_url='login')
# @user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient/patient_appointment.html',{'patient':patient})



@login_required(login_url='login')
# @user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=PatientAppointmentForm()
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    mydict={'appointmentForm':appointmentForm,'patient':patient}
    if request.method=='POST':
        appointmentForm=PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'patient/patient_book_appointment.html',context=mydict)





@login_required(login_url='login')
# @user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'patient/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='login')
# @user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
