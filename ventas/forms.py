from django.forms import ModelForm
from .models import VentasPrepago

class VentasPrepagoForm(ModelForm):
    class Meta:
        model = VentasPrepago
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'curp', 'dn', 'nip', ]