from django.urls import path
from patient import views
urlpatterns = [
    path('registration/', views.patient_registration,name='patient_registration'),
    path('dashboard', views.patient_dashboard_view,name='patient-dashboard'),
]
