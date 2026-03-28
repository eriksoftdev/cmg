from django.forms import ModelForm
from django import forms
from .models import VentaPrepago
from django.core.validators import RegexValidator

class VentaPrepagoForm(ModelForm):
    dn = forms.CharField(
        min_length=10,
        max_length=10,
        validators=[RegexValidator(r'^\d+$', 'Solo se permiten números')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'inputmode': 'numeric',
            'pattern': r'\d{10}',
            'required': True,
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',
            'maxlength': 10
        })
)
    nip = forms.CharField(
        min_length=4,
        max_length=4,
        validators=[RegexValidator(r'^\d+$', 'Solo se permiten números')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'inputmode': 'numeric',
            'pattern': r'\d{4}',
            'required': True,
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',
            'maxlength': 4
        })
    )
    class Meta:
        model = VentaPrepago
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'curp', 'dn', 'nip']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control'}),
        }


