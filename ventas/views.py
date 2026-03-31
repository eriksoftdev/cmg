from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VentaPrepagoForm
from .models import VentaPrepago
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

#region prepago 
# Agregar y mostrar ventas prepago
@login_required
def prepago(request):
    if request.method == 'GET':
        ventas_prepago = VentaPrepago.objects.filter(user=request.user, validar=False).order_by('-created')
        ventas_prepago_validadas = VentaPrepago.objects.filter(user=request.user, validar=True).order_by('-created')
        return render(request, 'prepago.html', {
        'form': VentaPrepagoForm(),
        'ventas_prepago': ventas_prepago,
        'ventas_prepago_validadas': ventas_prepago_validadas
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
            messages.error(request, '¡Error al crear la venta prepago!')
            return redirect('prepago')


#update venta prepago
@login_required
def update_venta_prepago(request, venta_prepago_id):
    venta_prepago = get_object_or_404(VentaPrepago, id=venta_prepago_id)
    if request.method == 'POST':
        venta_prepago.nombre = request.POST.get('nombre')
        venta_prepago.apellido_paterno = request.POST.get('apellido_paterno')
        venta_prepago.apellido_materno = request.POST.get('apellido_materno')
        venta_prepago.curp = request.POST.get('curp')
        venta_prepago.dn = request.POST.get('dn')
        venta_prepago.nip = request.POST.get('nip')
        venta_prepago.contact1 = request.POST.get('contact1')
        venta_prepago.contact2 = request.POST.get('contact2')
        venta_prepago.fvc = request.POST.get('fvc')
        venta_prepago.validar = 'validar' in request.POST
        venta_prepago.save()
        messages.success(request, '¡Venta prepago actualizada correctamente!')
        return redirect('prepago')
    return redirect('prepago')
        
# Eliminar venta prepago       
@login_required
def delete_venta_prepago(request, venta_prepago_id):
    venta_prepago = get_object_or_404(VentaPrepago, id=venta_prepago_id)
    venta_prepago.delete()
    messages.success(request, '¡Venta prepago eliminada!')
    return redirect('prepago')

# Agregar y mostrar ventas pospago
@login_required
def pospago(request):
    return render(request, 'pospago.html')

@login_required
def tarjetas(request):
    return render(request, 'tarjetas.html') 
