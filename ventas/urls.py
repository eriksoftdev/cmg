from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prepago/', views.prepago, name='prepago'),
    path('update_venta_prepago/<int:venta_prepago_id>/',
         views.update_venta_prepago, name='update_venta_prepago'),
    path('delete_venta_prepago/<int:venta_prepago_id>/',
         views.delete_venta_prepago, name='delete_venta_prepago'),
    path('pospago/', views.pospago, name='pospago'),
    path('update_venta_pospago/<int:venta_pospago_id>/',
         views.update_venta_pospago, name='update_venta_pospago'),
    path('delete_venta_pospago/<int:venta_pospago_id>/',
         views.delete_venta_pospago, name='delete_venta_pospago'),
]
