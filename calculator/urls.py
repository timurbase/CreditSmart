"""Calculator app URL configuration."""

from django.urls import path

from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate/', views.calculate, name='calculate'),
    path('compare/', views.compare, name='compare'),
    path('about/', views.about, name='about'),
]
