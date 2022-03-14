from django.urls import path
from dash import views

urlpatterns = [
    path('dashboard1', views.dashboard1),
    path('dashboard2', views.dashboard2),
    path('dashboard3', views.dashboard3),
]
