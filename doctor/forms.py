from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core import validators
from doctor.models import *
##documentation
#https://docs.djangoproject.com/en/3.1/ref/forms/validation/
#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
#https://docs.djangoproject.com/en/3.1/ref/validators/
#https://www.youtube.com/watch?v=7W58mD6sAhg&t=442s
##Create Django form using form api: https://www.youtube.com/watch?v=CtD4u-Bncf8
##How to Get Form Data and Validate Data: https://www.youtube.com/watch?v=xXZbxxH1jTQ
#Follow this for more widget modifications: https://www.youtube.com/watch?v=wVnQkKf-gHo
#check email form txt/json file:https://www.youtube.com/watch?v=fUbIjy1b_s8
#https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

class CreateUserForm(UserCreationForm):
    # error_css_class = 'error'
    # required_css_class = 'required'
    username=forms.CharField(error_messages={'required':'Enter an username'},widget=forms.TextInput(attrs={'placeholder':'Username'}))
    first_name=forms.CharField(error_messages={'required':'Enter your First Name'},widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name=forms.CharField(error_messages={'required':'Enter your last Name'},widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    password1=forms.CharField(label='Password',min_length=5, max_length=10,error_messages={'required':'Enter password'},widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(label='Password confirmation',min_length=5, max_length=10,error_messages={'required':'Enter confirmation password'},widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation'}))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        exclude = ['email']
        ##this will not work if we use forms.CharField() Already
        # labels = {
        #     'username': _('Username'),
        #     'first_name': 'First Name',
        #     'last_name': 'Last Name',
        #     'password1': 'Password',
        #     'password2': 'Password confirmation'
        # }
        # help_texts = {
        #     'username': _('User Name is not unique.'),
        # }
        # error_messages = {
        #     'username': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }
    ##Post django form cleaning.This part will not overwrite required
    # u = "milon"
    # if User.objects.filter(username=u).exists():
    #     print("name", u)
    def clean_username(self,*args, **kwargs):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User Already Exists.Try another one.")
        else:
            return username
    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     p1 = cleaned_data.get('password1')
    #     p2 = cleaned_data.get('password2')
    #     if p1 !=p2:
    #         raise forms.ValidationError("Password does not match.")
    #     return cleaned_data
    # def clean_username(self,*args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     if not email.endswith("edu"):
    #         raise forms.ValidationError("This email is not valid.")
    #     return email




class DoctorForm(forms.ModelForm):#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Rajpara, Rajshahi'}))
    mobile=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Phone number'}))
    department=forms.CharField(widget=forms.Select(choices=departments))
    #example: price = forms.DecimalField(initial=199.99)
    class Meta:
        model=Doctor
        fields=['address','mobile','department','status','profile_pic']
        exclude = ['user','status']
        #this labels will not work. if we use forms.CharField().Like we didn't use profile_pic.that's why here profile_pic label will noly work
        labels = {
            'address': _('Address'),
            'mobile': 'Phone Number',
            'department': 'Department',
            'profile_pic': 'Upload profile picture'
        }


    # def __init__(self, *args, **kwargs):
    #     super(EmployeeForm, self).__init__(*args, **kwargs)
    #     self.fields['position'].empty_label = "Select"
    #     #kono field ke required false kora
    #     self.fields['mobile'].required = False
