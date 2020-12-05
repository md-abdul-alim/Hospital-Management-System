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


class DoctorForm(forms.ModelForm):#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Rajpara, Rajshahi'}))
    mobile=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Phone number'}))
    department=forms.CharField(widget=forms.Select(choices=departments))
    #example: price = forms.DecimalField(initial=199.99)
    class Meta:
        model=Doctor
        fields=['address','mobile','department','profile_pic']
        exclude = ['user','status']
        #this labels will not work. if we use forms.CharField().Like we didn't use profile_pic.that's why here profile_pic label will noly work
        labels = {
            'address': _('Address'),
            'mobile': 'Phone Number',
            'department': 'Department',
            'profile_pic': 'Upload profile picture'
        }
    def clean_mobile(self,*args, **kwargs):
        mobile = self.cleaned_data.get("mobile")
        if Doctor.objects.filter(mobile=mobile).exists():
            #raise forms.ValidationError("User Already Exists.Try another one.")
            raise forms.ValidationError('This "%s" is already in use.' %mobile)
        else:
            return mobile

    # def __init__(self, *args, **kwargs):
    #     super(EmployeeForm, self).__init__(*args, **kwargs)
    #     self.fields['position'].empty_label = "Select"
    #     #kono field ke required false kora
    #     self.fields['mobile'].required = False
