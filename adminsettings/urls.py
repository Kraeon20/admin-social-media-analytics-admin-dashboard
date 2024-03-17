from django.urls import path
from . import views
from .views import reset_password


urlpatterns = [
    path('adminsettings/', views.settings_page, name='settings'),
    path('reset-password/', reset_password, name='reset-password'),
]
