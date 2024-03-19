# adminpanel/urls.py
from django.urls import path
from . import views
from .views import reset_password

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('admin_settings/', views.admin_settings, name='admin_settings'),
    path('reset-password/', reset_password, name='reset-password'),
    path('logout/', views.logout_view, name='logout'),

]
