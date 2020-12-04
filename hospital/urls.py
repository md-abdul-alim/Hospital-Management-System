from django.urls import path
from hospital import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),

    path('registration/', views.hopital_registration, name='hopital_registration'),
    path('dashboard', views.admin_dashboard_view,name='admin-dashboard'),
]
