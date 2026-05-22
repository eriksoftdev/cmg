from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User


numeric_validator = RegexValidator(r'^[0-9]*$', 'Solo se permiten números.')

# Create your models here.


class VentaPrepago(models.Model):
    nombre = models.CharField('NOMBRE(S)', max_length=100)
    apellido_paterno = models.CharField('APELLIDO PATERNO', max_length=100)
    apellido_materno = models.CharField(
        'APELLIDO MATERNO', max_length=100, blank=True, default='')
    curp = models.CharField('CURP', max_length=18, validators=[
                            MinLengthValidator(18)])
    dn = models.CharField('DN', max_length=10, validators=[
                          numeric_validator, MinLengthValidator(10)])
    nip = models.CharField('NIP', max_length=4, validators=[
                           numeric_validator, MinLengthValidator(4)], help_text='Solo se permiten números.')
    contact1 = models.CharField('CONTACTO1', max_length=16, validators=[
                                MinLengthValidator(10), RegexValidator(r'^[A-Z0-9 ]+$')])
    contact2 = models.CharField('CONTACTO 2', max_length=10, validators=[
                                numeric_validator, MinLengthValidator(10)])
    fvc = models.DateField('FVC')
    acepta_promo = models.BooleanField(
        'ACEPTA PROMO', null=True, blank=True, choices=[(True, 'Sí'), (False, 'No')])
    STATUS_CHOICES = [
        ('en_proceso', 'EN PROCESO'),
        ('nip_incorrecto', 'NIP INCORRECTO'),
        ('curp_incorrecto', 'CURP INCORRECTO'),
        ('sin_fvc', 'SIN FVC'),
        ('exitosa', 'EXITOSA'),
        ('baja_exportada', 'BAJA EXPORTADA'),
        ('alta', 'ALTA'),
        ('gestionada_por_otro_call_center', 'GESTIONADA POR OTRO CALL CENTER'),
        ('sin_nip', 'SIN NIP'),
        ('futura', 'FUTURA'),
        ('linea_movistar', 'LINEA MOVISTAR'),
        ('cac_lejano', 'CAC LEJANO'),
    ]

    status = models.CharField(
        'Status',
        max_length=100,
        choices=STATUS_CHOICES,
        default='en_proceso'
    )
    email = models.EmailField('EMAIL', max_length=254)
    folio = models.CharField('FOLIO', max_length=100)
    usuario_marcador = models.CharField('USUARIO MARCADOR', max_length=100)
    marcador = models.CharField('MARCADOR', max_length=100)
    validador = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validador')
    supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervisor')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vendedor')

# region Pospago


class VentaPospago(models.Model):
    nombre = models.CharField('NOMBRE(S)', max_length=100)
    apellido_paterno = models.CharField('APELLIDO PATERNO', max_length=100)
    apellido_materno = models.CharField(
        'APELLIDO MATERNO', max_length=100, blank=True, default='')
    curp = models.CharField('CURP', max_length=18, validators=[
        MinLengthValidator(18)])
    rfc = models.CharField('RFC', max_length=13, validators=[
                           MinLengthValidator(13)])
    identificacion = models.CharField('IDENTIFICACIÓN', max_length=15, validators=[
        MinLengthValidator(15)])
    dn = models.CharField('DN', max_length=10, validators=[
        numeric_validator, MinLengthValidator(10)])
    nip = models.CharField('NIP', max_length=4, validators=[
        numeric_validator, MinLengthValidator(4)], help_text='Solo se permiten números.')
    contact1 = models.CharField('CONTACTO1', max_length=16, validators=[
        MinLengthValidator(10), RegexValidator(r'^[A-Z0-9 ]+$')])
    contact2 = models.CharField('CONTACTO 2', max_length=10, validators=[
        numeric_validator, MinLengthValidator(10)])
    plan_choices = [
        ('pro_8', 'PRO 8'),
        ('pro_10', 'PRO 10'),
        ('pro_14', 'PRO 14'),
        ('pro_18', 'PRO 18'),
        ('pro_25', 'PRO 25'),
        ('pro_35', 'PRO 35'),
        ('pro_ilimitado', 'PRO ILIMITADO'),
    ]
    plan = models.CharField(
        'PLAN',
        max_length=20,
        choices=plan_choices,
    )
    cac = models.CharField('CAC', max_length=100)
    cp = models.CharField('CP', max_length=5, validators=[
        numeric_validator, MinLengthValidator(5)])
    fecha_nacimiento = models.DateField('FECHA DE NACIMIENTO')
    estado_republica_choices = [
        ('AGUASCALIENTES', 'AGUASCALIENTES'),
        ('BAJA CALIFORNIA', 'BAJA CALIFORNIA'),
        ('BAJA CALIFORNIA SUR', 'BAJA CALIFORNIA SUR'),
        ('CAMPECHE', 'CAMPECHE'),
        ('COAHUILA', 'COAHUILA'),
        ('COLIMA', 'COLIMA'),
        ('CHIAPAS', 'CHIAPAS'),
        ('CHIHUAHUA', 'CHIHUAHUA'),
        ('CIUDAD DE MEXICO', 'CIUDAD DE MEXICO'),
        ('DURANGO', 'DURANGO'),
        ('GUANAJUATO', 'GUANAJUATO'),
        ('GUERRERO', 'GUERRERO'),
        ('HIDALGO', 'HIDALGO'),
        ('JALISCO', 'JALISCO'),
        ('MEXICO', 'MEXICO'),
        ('MICHOACAN', 'MICHOACAN'),
        ('MORELOS', 'MORELOS'),
        ('NAYARIT', 'NAYARIT'),
        ('NUEVO LEON', 'NUEVO LEON'),
        ('OAXACA', 'OAXACA'),
        ('PUEBLA', 'PUEBLA'),
        ('QUERETARO', 'QUERETARO'),
        ('QUINTANA ROO', 'QUINTANA ROO'),
        ('SAN LUIS POTOSI', 'SAN LUIS POTOSI'),
        ('SINALOA', 'SINALOA'),
        ('SONORA', 'SONORA'),
        ('TABASCO', 'TABASCO'),
        ('TAMAULIPAS', 'TAMAULIPAS'),
        ('TLAXCALA', 'TLAXCALA'),
        ('VERACRUZ', 'VERACRUZ'),
        ('YUCATAN', 'YUCATAN'),
        ('ZACATECAS', 'ZACATECAS'),
    ]
    estado_republica = models.CharField(
        'ESTADO DE LA REPUBLICA',
        max_length=20,
        choices=estado_republica_choices,
    )
    municipio = models.CharField('MUNICIPIO', max_length=100)
    colonia = models.CharField('COLONIA', max_length=100)
    calle = models.CharField('CALLE', max_length=100)
    numero_exterior = models.CharField('NUMERO EXTERIOR', max_length=20)
    numero_interior = models.CharField(
        'NUMERO INTERIOR', max_length=20, blank=True, default=''
    )
    fvc = models.DateField('FVC')
    email = models.EmailField('EMAIL', max_length=254)
    status_choices = [
        ('en_proceso', 'EN PROCESO'),
        ('rechazo_nip', 'RECHAZO NIP'),
        ('rechazo_magento', 'RECHAZO MAGENTO'),
        ('black_list', 'BLACK LIST'),
        ('datos_incorrectos', 'DATOS INCORRECTOS'),
        ('exitosa', 'EXITOSA'),
        ('linea_movistar', 'LINEA MOVISTAR'),
        ('gestionada_por_otro_call_center', 'GESTIONADA POR OTRO CALL CENTER'),
        ('alta', 'ALTA'),
        ('cancelacion', 'CANCELACIÓN'),
    ]
    status_pospago = models.CharField(
        'STATUS',
        max_length=100,
        choices=status_choices,
        default='en_proceso'
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vendedor_pospago')
    supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervisor_pospago')
