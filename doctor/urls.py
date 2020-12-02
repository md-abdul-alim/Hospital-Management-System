from django.urls import path
from doctor import views
urlpatterns = [
    path('registration/', views.doctor_registration,name='doctor_registration'),
]
