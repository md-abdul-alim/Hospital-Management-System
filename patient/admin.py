from django.contrib import admin
from .models import Patient
# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)
