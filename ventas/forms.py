from django.forms import ModelForm
from django import forms
from .models import VentaPrepago
from django.core.validators import RegexValidator
from datetime import date

class VentaPrepagoForm(ModelForm):
    dn = forms.CharField(
        label='DN',
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

    contact1 = forms.CharField(
        label='CONTACTO 1',
        min_length=10,
        max_length=16,
        validators=[
        RegexValidator(
            r'^[A-Z0-9 ]{10,16}$', 
            message='El contacto debe tener entre 10 y 16 caracteres (solo letras mayúsculas y números).'
        )
    ],
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'inputmode': 'text',  
        'pattern': r'[A-Z0-9 ]{10,16}', 
        'required': True,
        'oninput': "this.value = this.value.toUpperCase().replace(/[^A-Z0-9 ]/g, '')",
    })
)
    
    contact2 = forms.CharField(
        label='CONTACTO 2',
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
        label='NIP',
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

    curp = forms.CharField(
        label='CURP',
        min_length=18,
        max_length=18,
        validators=[RegexValidator(
            r'^[A-Z0-9]{18}$', 
            'El CURP debe tener exactamente 18 caracteres alfanuméricos.'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'text-transform: uppercase;',
            'oninput': 'this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "")',
            'maxlength': 18, 
            'required':True,
            'pattern': r'^[A-Z0-9]{18}$'
        })
    )


    class Meta:
        model = VentaPrepago
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'curp', 'dn', 'nip', 'fvc','contact1', 'contact2', 'email', 'folio','usuario_marcador','marcador', 'acepta_promo', 'status']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'fvc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': date.today().isoformat()}, format='%Y-%m-%d'),
            'acepta_promo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'text-transform: lowercase;', 'oninput': 'this.value = this.value.toLowerCase()'}),
            'folio': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'}),
            'usuario_marcador': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'}),
            'marcador': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'}),
        }

#Validacion para que los datos nombre, apellidos y curp se guarden en mayusculas para prepago

# Validaciones para guardar siempre en MAYÚSCULAS
    def clean_nombre(self):
        return self.cleaned_data.get('nombre', '').upper()

    def clean_apellido_paterno(self):
        return self.cleaned_data.get('apellido_paterno', '').upper()

    def clean_apellido_materno(self):
        # Aquí sí conviene el if porque este campo puede ser opcional (null=True)
        val = self.cleaned_data.get('apellido_materno')
        return val.upper() if val else val

    def clean_curp(self):
        return self.cleaned_data.get('curp', '').upper()
    
    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()