from django.urls import path
from . import views
# hChart.urls.py
from django.contrib import admin

from django.urls import path
from accounts import views
from django.urls import path, include # !!!
from django.contrib.auth import urls
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
