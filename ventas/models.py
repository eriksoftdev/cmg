from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User


numeric_validator = RegexValidator(r'^[0-9]*$', 'Solo se permiten números.')

# Create your models here.
class VentaPrepago(models.Model):
    nombre = models.CharField('NOMBRE(S)',max_length=100)
    apellido_paterno = models.CharField('APELLIDO PATERNO', max_length=100)
    apellido_materno = models.CharField('APELLIDO MATERNO', max_length=100,blank=True, default='')
    curp = models.CharField('CURP', max_length=18,validators=[MinLengthValidator(18)])
    dn = models.CharField('DN', max_length=10, validators=[numeric_validator, MinLengthValidator(10)])
    nip = models.CharField('NIP', max_length=4, validators=[numeric_validator, MinLengthValidator(4)], help_text='Solo se permiten números.')
    contact1 = models.CharField('CONTACTO1', max_length=16, validators=[MinLengthValidator(10), RegexValidator(r'^[A-Z0-9 ]+$')])
    contact2 = models.CharField('CONTACTO 2', max_length=10, validators=[numeric_validator, MinLengthValidator(10)])
    fvc = models.DateField('FVC')
    acepta_promo = models.BooleanField('ACEPTA PROMO', null=True, blank=True, choices=[(True, 'Sí'), (False, 'No')])
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
    validador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validador')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor')