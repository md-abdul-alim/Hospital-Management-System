from django.urls import path
from hospital import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login/',views.loginPage,name='login'),
]
