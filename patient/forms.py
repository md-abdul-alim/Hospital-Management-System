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
            #raise forms.ValidationError("User Already Exists.Try another one.")
            raise forms.ValidationError('Username "%s" is already in use.' %username)
        else:
            return username

    ##here both password1 & password2 clean data is working well.we just comment it because it cannot validate miss match password

    def clean_password1(self,*args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        if len(password1)<8:
            raise forms.ValidationError('This password is too short. It must contain at least 8 characters.')
        return password1

    def clean_password2(self): #https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print("pass1", password1)
        if len(password2)<8:
            raise forms.ValidationError('This password is too short. It must contain at least 8 characters.')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_first_name(self,*args, **kwargs):
        first_name = self.cleaned_data.get("first_name")
        #return pass1
        if first_name == "" :
            raise forms.ValidationError('First name can not be empty.')
        return first_name

    def clean_last_name(self,*args, **kwargs):
        last_name = self.cleaned_data.get("last_name")
        #return pass1
        if last_name == "" :
            raise forms.ValidationError('Last name can not be empty.')
        return last_name

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
    symptoms=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Symptoms'}))

    assignedDoctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=Patient
        fields=['address','mobile','status','symptoms','profile_pic']
        exclude = ['user']
        labels = {
            'mobile': _('Phone Number'),#this will not work because previously we used customized upper
            #'status': 'Status',
            'profile_pic': 'Upload profile picture'
        }
    def clean_mobile(self,*args, **kwargs):
        mobile = self.cleaned_data.get("mobile")
        if Patient.objects.filter(mobile=mobile).exists():
            #raise forms.ValidationError("User Already Exists.Try another one.")
            raise forms.ValidationError('This "%s" is already in use.' %mobile)
        else:
            return mobile

    def clean_symptoms(self,*args, **kwargs):
        symptoms = self.cleaned_data.get("symptoms")
        if len(symptoms)<5:
            raise forms.ValidationError('Please provide some symptoms.')
        return symptoms
