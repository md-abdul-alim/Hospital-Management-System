from django.urls import path
from hospital import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login/',views.loginPage,name='login'),

    path('registration/', views.hopital_registration, name='hopital_registration'),
    path('registration/', views.doctor_registration,name='doctor_registration'),
    path('registration/', views.patient_registration, name='patient_registration'),
]
