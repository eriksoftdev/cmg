from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('prepago/', views.prepago),
    path('tarjetas/', views.tarjetas),
    path('pospago/', views.pospago),
]