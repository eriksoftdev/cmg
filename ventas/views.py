from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import VentaPrepagoForm
from .models import VentaPrepago
from django.contrib import messages
from django.urls import reverse
# para ver que se no se envien los mismo registros import time
# import time

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# region prepago
# Agregar y mostrar ventas prepago


@login_required
def prepago(request):
    es_vendedor = request.user.groups.filter(name='VENDEDORES').exists()
    # Definimos la jerarquía: Tú (superuser) o el personal de oficina (Validadores/Supervisores)
    es_superior = request.user.is_superuser or request.user.groups.filter(
        name__in=['VALIDADORES', 'SUPERVISORES']).exists()
    es_supervisor = request.user.is_superuser or request.user.groups.filter(
        name='SUPERVISORES').exists()

    # Definimos el rol activo  por si cambia entre superior a vendedor o viceversa
    if es_superior:
        if request.GET.get('rol'):
            request.session['rol_activo'] = request.GET.get('rol')

        if request.session.get('rol_activo') == 'vendedor':
            es_supervisor = False
            es_vendedor = True
        else:
            es_vendedor = False
            pass  # El rol activo sigue siendo el de superior, no hacemos cambios

    else:
        # Por defecto, si no es superior, es vendedor
        request.session['rol_activo'] = 'vendedor'
        es_vendedor = True
        es_supervisor = False
        es_supervisor = False

    if request.method == 'GET':
        # FILTRO MAESTRO
        if es_superior:
            base_queryset = VentaPrepago.objects.all()
        else:
            base_queryset = VentaPrepago.objects.filter(user=request.user)

        # Segmentación para los tabs de la interfaz
        ventas_prepago = base_queryset.filter(
            acepta_promo=None).order_by('-created')

        ventas_prepago_validadas = base_queryset.filter(
            acepta_promo=True, status='en_proceso').order_by('-created')

        ventas_prepago_exitosas = base_queryset.filter(
            status='exitosa').order_by('-created')

        ventas_prepago_rechazos_promo = base_queryset.filter(
            acepta_promo=False).order_by('-created')

        ventas_prepago_rechazos = base_queryset.exclude(acepta_promo=None).exclude(
            status='exitosa').exclude(status='en_proceso').order_by('-created')

        return render(request, 'prepago.html', {
            'form': VentaPrepagoForm(user=request.user, rol_activo=request.session.get('rol_activo')),
            'ventas_prepago': ventas_prepago,
            'ventas_prepago_validadas': ventas_prepago_validadas,
            'ventas_prepago_exitosas': ventas_prepago_exitosas,
            'ventas_prepago_rechazos_promo': ventas_prepago_rechazos_promo,
            'ventas_prepago_rechazos': ventas_prepago_rechazos,
            'es_superior': es_superior,  # Pasamos esta bandera al HTML
            'es_supervisor': es_supervisor,  # Pasamos esta bandera al HTML
            'es_vendedor': es_vendedor  # Pasamos esta bandera al HTML
        })

    # Lógica POST para crear ventas (El común siempre entra aquí)
    else:
        # Evitamos que se envien los mismo registros
        form_data = request.POST.get('curp') + request.POST.get('dn')
        if request.session.get('last_form') == form_data:
            return redirect('prepago')

        form = VentaPrepagoForm(request.POST, user=request.user)
        if form.is_valid():
            new_venta = form.save(commit=False)
            new_venta.user = request.user  # El dueño siempre es quien está logueado
            # time.sleep(10)
            new_venta.save()
            request.session['last_form'] = form_data
            messages.success(request, '¡Venta registrada!')
        return redirect('prepago')

# update venta prepago


@login_required
@permission_required('ventas.change_ventaprepago', raise_exception=True)
def update_venta_prepago(request, venta_prepago_id):
    es_superior = request.user.is_superuser or request.user.groups.filter(
        name__in=['VALIDADORES', 'SUPERVISORES']).exists()
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
        venta_prepago.email = request.POST.get('email')
        venta_prepago.folio = request.POST.get('folio')
        venta_prepago.usuario_marcador = request.POST.get('usuario_marcador')
        venta_prepago.marcador = request.POST.get('marcador')

        # Lógica de Validación Única
        if 'acepta_promo' in request.POST:
            if es_superior:
                if venta_prepago.acepta_promo is None or request.user.is_superuser:
                    valor = request.POST.get('acepta_promo')
                    if valor == 'True':
                        venta_prepago.acepta_promo = True
                    elif valor == 'False':
                        venta_prepago.acepta_promo = False
                    else:
                        venta_prepago.acepta_promo = None

                    if not venta_prepago.validador:
                        venta_prepago.validador = request.user
                    messages.success(
                        request, '¡Venta prepago validada correctamente!')
                else:
                    valor = request.POST.get('acepta_promo') == 'True'
                    if valor != venta_prepago.acepta_promo:
                        messages.error(request, '¡La venta ya fue validada!')

        if 'status' in request.POST:
            # Solo permitimos cambiar el status si es Supervisor o Admin
            if request.user.is_superuser or request.user.groups.filter(name='SUPERVISORES').exists():
                venta_prepago.status = request.POST.get('status')

        venta_prepago.save()
        tab = request.GET.get('tab', 'ventas')
        messages.success(request, '¡Venta prepago actualizada correctamente!')
        return redirect(f"{reverse('prepago')}?tab={tab}")
    return redirect('prepago')

# Eliminar venta prepago


@login_required
@permission_required('ventas.delete_ventaprepago', raise_exception=True)
def delete_venta_prepago(request, venta_prepago_id):
    venta_prepago = get_object_or_404(VentaPrepago, id=venta_prepago_id)
    venta_prepago.delete()
    messages.success(request, '¡Venta prepago eliminada!')
    tab = request.GET.get('tab', 'ventas')
    return redirect(f"{reverse('prepago')}?tab={tab}")
# endregion


# region pospago
# Agregar y mostrar ventas pospago
@login_required
def pospago(request):
    return render(request, 'pospago.html')


@login_required
def tarjetas(request):
    return render(request, 'tarjetas.html')
# endregion
