from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

def redirectlogin(request):
    user = request.user
    # if user.is_authenticated:  # if : if the user is logged in already and trying to access login again
    if user.groups.filter(name='ADMIN').exists():
        login(request, user)
        return redirect('admin-dashboard')
    elif user.groups.filter(name='DOCTOR').exists():
        login(request, user)
        return redirect('doctor-dashboard')
    elif user.groups.filter(name='PATIENT').exists():
        login(request, user)
        return redirect('patient-dashboard')
