from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VentaPrepagoForm
from .models import VentaPrepago
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def prepago(request):
    if request.method == 'GET':
        ventas_prepago = VentaPrepago.objects.filter(user=request.user).order_by('-created')
        return render(request, 'prepago.html', {
        'form': VentaPrepagoForm(),
        'ventas_prepago': ventas_prepago
    })
    else:
        form = VentaPrepagoForm(request.POST)
        if form.is_valid():
            new_venta_prepago = form.save(commit=False)
            new_venta_prepago.user = request.user
            new_venta_prepago.save()
            messages.success(request, '¡Venta prepago creada con éxito!')
            return redirect('prepago')
        else:
            messages.error(request, '¡Error al crear la nota!')
            return redirect('prepago')

@login_required
def pospago(request):
    return render(request, 'pospago.html')

@login_required
def tarjetas(request):
    return render(request, 'tarjetas.html') 
