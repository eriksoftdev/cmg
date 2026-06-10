from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import VentaPrepagoForm
from .models import VentaPrepago, User
from .forms_pospago import VentaPospagoForm
from .models import VentaPospago
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

# se muestran las ventas segun el rol y el filtro por usuario
    if request.method == 'GET':
        ventas_prepago_usuario = request.GET.get('ventas_prepago_usuario')
        # FILTRO MAESTRO
        if es_superior:
            if ventas_prepago_usuario:
                base_queryset = VentaPrepago.objects.filter(
                    user_id=ventas_prepago_usuario)
            else:
                base_queryset = VentaPrepago.objects.all()
        else:
            base_queryset = VentaPrepago.objects.filter(user=request.user)

        # Para la ui de filtrar fechas
        fecha_inicio = request.GET.get('fechaInicio')
        fecha_fin = request.GET.get('fechaFin')

        if fecha_inicio:
            base_queryset = base_queryset.filter(
                created__date__gte=fecha_inicio)

        if fecha_fin:
            base_queryset = base_queryset.filter(created__date__lte=fecha_fin)

        filtro_dn = request.GET.get('dn', '').strip()
        if filtro_dn:
            base_queryset = base_queryset.filter(dn=filtro_dn)

        filtro_curp = request.GET.get('curp', '').strip().upper()
        if filtro_curp:
            base_queryset = base_queryset.filter(curp=filtro_curp)

        filtro_folio = request.GET.get('folio', '').strip().upper()
        if filtro_folio:
            base_queryset = base_queryset.filter(folio=filtro_folio)

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

        # exportar a csv

        if request.GET.get('exportar') == 'true':
            import csv
            from django.http import HttpResponse

            response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
            response['Content-Disposition'] = 'attachment; filename="ventas_prepago.csv"'

            writer = csv.writer(response)

            writer.writerow(['CLIENTE', 'CURP', 'DN', 'NIP',
                            'CONTACTO 1', 'CONTACTO 2', 'EMAIL', 'FVC', 'VENDEDOR', 'VICIDIAL', 'FOLIO', 'USUARIO MARCADOR', 'CREADO'])
            for venta_prepago in base_queryset.order_by('-created'):
                cliente = f"{venta_prepago.nombre} {venta_prepago.apellido_paterno} {venta_prepago.apellido_materno}".strip()
                writer.writerow([cliente, venta_prepago.curp,
                                venta_prepago.dn, venta_prepago.nip, venta_prepago.contact1,
                                venta_prepago.contact2, venta_prepago.email, venta_prepago.fvc.strftime('%d-%m-%Y'), venta_prepago.user.get_full_name(), venta_prepago.marcador, venta_prepago.folio, venta_prepago.usuario_marcador, venta_prepago.created.strftime('%d-%m-%Y %H:%M:%S')])
            return response

        return render(request, 'prepago.html', {
            'form': VentaPrepagoForm(user=request.user, rol_activo=request.session.get('rol_activo')),
            'ventas_prepago': ventas_prepago,
            'ventas_prepago_validadas': ventas_prepago_validadas,
            'ventas_prepago_exitosas': ventas_prepago_exitosas,
            'ventas_prepago_rechazos_promo': ventas_prepago_rechazos_promo,
            'ventas_prepago_rechazos': ventas_prepago_rechazos,
            'es_superior': es_superior,  # Pasamos esta bandera al HTML
            'es_supervisor': es_supervisor,  # Pasamos esta bandera al HTML
            'es_vendedor': es_vendedor,  # Pasamos esta bandera al HTML
            'fecha_inicio': fecha_inicio,  # Para mantener el filtro en la interfaz
            'fecha_fin': fecha_fin,  # Para mantener el filtro en la interfaz
            # para obtener los users del sistema importando User del model
            'usuarios': User.objects.filter(is_active=True).order_by('username'),
            # Para mantener el filtro en la interfaz
            'ventas_prepago_usuario': ventas_prepago_usuario,
            'filtro_dn': filtro_dn,
            'filtro_curp': filtro_curp,
            'filtro_folio': filtro_folio,
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
    es_vendedor = request.user.groups.filter(name='VENDEDORES').exists()
    es_supervisor = request.user.is_superuser or request.user.groups.filter(
        name='SUPERVISORES').exists()

    # Definimos el rol activo  por si cambia entre supervisor a vendedor o viceversa
    if es_supervisor:
        if request.GET.get('rol'):
            request.session['rol_activo'] = request.GET.get('rol')

        if request.session.get('rol_activo') == 'vendedor':
            es_supervisor = False
            es_vendedor = True
        else:
            es_vendedor = False
            pass  # El rol activo sigue siendo el de supervisor, no hacemos cambios
    else:
        # Por defecto, si no es supervisor, es vendedor
        request.session['rol_activo'] = 'vendedor'
        es_vendedor = True
        es_supervisor = False

    if request.method == 'GET':
        # FILTRO MAESTRO
        if es_supervisor:
            base_queryset = VentaPospago.objects.all()
        else:
            base_queryset = VentaPospago.objects.filter(user=request.user)

        # Segmentación para los tabs de la interfaz
        ventas_pospago = base_queryset.filter(
            status_pospago='en_proceso').order_by('-created')

        ventas_pospago_exitosas = base_queryset.filter(
            status_pospago='exitosa').order_by('-created'
                                               )
        ventas_pospago_rechazos = base_queryset.exclude(
            status_pospago='en_proceso').exclude(status_pospago='exitosas').order_by('-created')

        return render(request, 'pospago.html', {
            'form': VentaPospagoForm(user=request.user, rol_activo=request.session.get('rol_activo')),
            'ventas_pospago': ventas_pospago,
            'es_supervisor': es_supervisor,  # Pasamos esta bandera al HTML
            'es_vendedor': es_vendedor,  # Pasamos esta bandera al HTML
            # Pasamos esta bandera al HTML para cambiar entre supervisor y vendedor
            'es_supervisor': request.user.is_superuser or request.user.groups.filter(name='SUPERVISORES').exists(),
            'ventas_pospago_exitosas': ventas_pospago_exitosas,
            'ventas_pospago_rechazos': ventas_pospago_rechazos,
        })
    else:
        # Evitamos que se envien los mismo registros
        form_data = request.POST.get('curp') + request.POST.get('dn')
        if request.session.get('last_form') == form_data:
            return redirect('pospago')

        form = VentaPospagoForm(request.POST, user=request.user)
        if form.is_valid():
            new_venta = form.save(commit=False)
            new_venta.user = request.user  # El dueño siempre es quien está logueado
            new_venta.save()
            request.session['last_form'] = form_data
            messages.success(request, '¡Venta registrada!')
        return redirect('pospago')

# update venta pospago


@login_required
@permission_required('ventas.change_ventapospago', raise_exception=True)
def update_venta_pospago(request, venta_pospago_id):
    es_supervisor = request.user.is_superuser or request.user.groups.filter(
        name__in=['SUPERVISORES']).exists()
    venta_pospago = get_object_or_404(VentaPospago, id=venta_pospago_id)
    if request.method == 'POST':
        venta_pospago.nombre = request.POST.get('nombre')
        venta_pospago.apellido_paterno = request.POST.get('apellido_paterno')
        venta_pospago.apellido_materno = request.POST.get('apellido_materno')
        venta_pospago.curp = request.POST.get('curp')
        venta_pospago.rfc = request.POST.get('rfc')
        venta_pospago.identificacion = request.POST.get('identificacion')
        venta_pospago.dn = request.POST.get('dn')
        venta_pospago.nip = request.POST.get('nip')
        venta_pospago.contact1 = request.POST.get('contact1')
        venta_pospago.contact2 = request.POST.get('contact2')
        venta_pospago.fvc = request.POST.get('fvc')
        venta_pospago.email = request.POST.get('email')
        venta_pospago.plan = request.POST.get('plan')
        venta_pospago.cac = request.POST.get('cac')
        venta_pospago.cp = request.POST.get('cp')
        venta_pospago.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        venta_pospago.estado_republica = request.POST.get('estado_republica')
        venta_pospago.municipio = request.POST.get('municipio')
        venta_pospago.colonia = request.POST.get('colonia')
        venta_pospago.calle = request.POST.get('calle')
        venta_pospago.numero_exterior = request.POST.get('numero_exterior')
        venta_pospago.numero_interior = request.POST.get('numero_interior')

        if 'status_pospago' in request.POST:
            if request.user.is_superuser or request.user.groups.filter(name='SUPERVISORES').exists():
                if venta_pospago.status_pospago == 'en_proceso' or request.user.is_superuser:
                    venta_pospago.status_pospago = request.POST.get(
                        'status_pospago')
                else:
                    messages.error(
                        request, 'No se puede modificar el status de la venta')

        venta_pospago.save()
        tab = request.GET.get('tab', 'ventas')
        messages.success(request, '¡Venta pospago actualizada correctamente!')
        return redirect(f"{reverse('pospago')}?tab={tab}")
    return redirect('pospago')
# delete venta pospago


@login_required
@permission_required('ventas.delete_ventapospago', raise_exception=True)
def delete_venta_pospago(request, venta_pospago_id):
    venta_pospago = get_object_or_404(VentaPospago, id=venta_pospago_id)
    venta_pospago.delete()
    messages.success(request, '¡Venta pospago eliminada!')
    tab = request.GET.get('tab', 'ventas')
    return redirect(f"{reverse('pospago')}?tab={tab}")
# endregion
