from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_ventas_prepago),
    path('tarjetas/', views.index_ventas_tarjetas),
    path('pospago/', views.index_ventas_pospago),
]