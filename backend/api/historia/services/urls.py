from django.urls import path
from . import views

urlpatterns = [
    path('historia/', views.historia_academica, name='historia'),
]