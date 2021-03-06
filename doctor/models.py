from django.db import models
from django.contrib.auth.models import User

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
#All model fields: https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
class Doctor(models.Model):
    user=models.OneToOneField(User,null=True, blank=True,on_delete=models.CASCADE)
    #https://docs.djangoproject.com/en/3.1/ref/forms/api/#binding-uploaded-files
    profile_pic= models.ImageField(upload_to='profile_pictures/Doctor_Profile_pictures/',null=True,blank=True)
    address = models.CharField(max_length=40,null=True,blank=True)
    mobile = models.CharField(max_length=20,null=True,blank=True,help_text='Use number only',)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)
