from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prepago/', views.prepago, name='prepago'),
    path('tarjetas/', views.tarjetas, name='tarjetas'),
    path('pospago/', views.pospago, name='pospago'),
]