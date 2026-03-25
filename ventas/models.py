from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User


numeric_validator = RegexValidator(r'^[0-9]*$', 'Solo se permiten números.')

# Create your models here.
class VentasPrepago(models.Model):
    nombre = models.CharField('Nombre(s)',max_length=100)
    apellido_paterno = models.CharField('Apellido Paterno', max_length=100)
    apellido_materno = models.CharField('Apellido Materno', max_length=100,blank=True, null=True)
    curp = models.CharField('CURP', max_length=18,validators=[MinLengthValidator(18)])
    dn = models.CharField('DN', max_length=10, validators=[numeric_validator, MinLengthValidator(10)])
    nip = models.CharField('NIP', max_length=4, validators=[numeric_validator, MinLengthValidator(4)], help_text='Solo se permiten números.')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)