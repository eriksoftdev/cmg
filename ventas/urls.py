from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prepago/', views.prepago, name='prepago'),
    path('delete_venta_prepago/<int:venta_prepago_id>/', views.delete_venta_prepago, name='delete_venta_prepago'),
    path('tarjetas/', views.tarjetas, name='tarjetas'),
    path('pospago/', views.pospago, name='pospago'),
]