from django.urls import path
from . import views

urlpatterns = [
    path('register_device/', views.register_device, name='register_device'),
]
