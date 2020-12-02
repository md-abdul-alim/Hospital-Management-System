from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from doctor.models import *

class CreateUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    password1=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Password confirmation'}))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        exclude = ['email']

    # def __init__(self, *args, **kwargs):
    #     super(CreateUserForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].required = False


class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['address','mobile','department','status','profile_pic']
        labels = {
            'address': 'Address',
            'mobile': 'Phone Number',
            'department': 'Department',
            'profile_pic': 'Upload profile picture'
        }
        exclude = ['user','status']

    # def __init__(self, *args, **kwargs):
    #     super(EmployeeForm, self).__init__(*args, **kwargs)
    #     self.fields['position'].empty_label = "Select"
    #     #kono field ke required false kora
    #     self.fields['mobile'].required = False
