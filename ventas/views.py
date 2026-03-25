from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VentasPrepagoForm
from .models import VentasPrepago
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def prepago(request):
    return render(request, 'prepago.html')

@login_required
def pospago(request):
    return render(request, 'pospago.html')

@login_required
def tarjetas(request):
    return render(request, 'tarjetas.html') 
