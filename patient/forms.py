from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core import validators
from patient.models import *
from doctor.models import *


class CreateUserForm(UserCreationForm):

    username=forms.CharField(error_messages={'required':'Enter an username'},widget=forms.TextInput(attrs={'placeholder':'Username'}))
    first_name=forms.CharField(error_messages={'required':'Enter your First Name'},widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name=forms.CharField(error_messages={'required':'Enter your last Name'},widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    password1=forms.CharField(label='Password',min_length=5, max_length=10,error_messages={'required':'Enter password'},widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(label='Password confirmation',min_length=5, max_length=10,error_messages={'required':'Enter confirmation password'},widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation'}))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        exclude = ['email']

    def clean_username(self,*args, **kwargs):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            print("beforeusername", username)
            #raise forms.ValidationError("User Already Exists.Try another one.")
            raise forms.ValidationError('Username "%s" is already in use.' %username)
            print("afterusername", username)
        else:
            return username

    def clean_password1(self,*args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        #return pass1
        if password1 != password2 :
            print("password check")
            raise forms.ValidationError('Password does not match.')

    # def clean_username(self):
    #     if self.is_valid():
    #         username = self.cleaned_data['username']
    #         #print("username", username)
    #         try:
    #             user = User.objects.exclude(pk=self.instance.pk).get(username=username)
    #             #print("username", username)
    #             raise forms.ValidationError('Username "%s" is already in use.' % username)
    #             print("username", username)
    #         except User.DoesNotExist:
    #             print("No username", username)
    #             return username
    #         #raise forms.ValidationError('Username "%s" is already in use.' % username)


class PatientForm(forms.ModelForm):#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Rajpara, Rajshahi'}))
    mobile=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Phone number'}))
    assignedDoctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=Patient
        fields=['address','mobile','status','symptoms','profile_pic']
        exclude = ['user']
