from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_notas, name='notas'),
]