from django.forms import ModelForm
from .models import VentaPrepago

class VentaPrepagoForm(ModelForm):
    class Meta:
        model = VentaPrepago
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'curp', 'dn', 'nip', ]