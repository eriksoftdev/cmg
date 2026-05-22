from django.forms import ModelForm
from django import forms
from .models import VentaPospago
from django.core.validators import RegexValidator
from datetime import date


class VentaPospagoForm(ModelForm):
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
            'required': True,
            'pattern': r'^[A-Z0-9]{18}$'
        })
    )

    rfc = forms.CharField(
        label='RFC',
        min_length=13,
        max_length=13,
        validators=[RegexValidator(
            r'^[A-Z0-9]{13}$',
            'El RFC debe tener exactamente 13 caracteres alfanuméricos.'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'text-transform: uppercase;',
            'oninput': 'this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "")',
            'maxlength': 13,
            'required': True,
            'pattern': r'^[A-Z0-9]{13}$'
        })
    )

    identificacion = forms.CharField(
        label='IDENTIFICACION',
        min_length=15,
        max_length=15,
        validators=[RegexValidator(
            r'^[A-Z0-9]{15}$',
            'La identificación debe tener exactamente 15 caracteres alfanuméricos.'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'text-transform: uppercase;',
            'oninput': 'this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "")',
            'maxlength': 15,
            'required': True,
            'pattern': r'^[A-Z0-9]{15}$'
        })
    )

    cp = forms.CharField(
        label='CP',
        min_length=5,
        max_length=5,
        validators=[RegexValidator(r'^\d+$', 'Solo se permiten números')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'inputmode': 'numeric',
            'pattern': r'\d{5}',
            'required': True,
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',
            'maxlength': 5
        })
    )

    class Meta:
        model = VentaPospago
        fields = ['nombre', 'apellido_paterno',
                  'apellido_materno', 'curp', 'fecha_nacimiento', 'rfc', 'identificacion',  'dn', 'fvc', 'nip', 'contact1', 'contact2', 'plan', 'email', 'cp', 'estado_republica',
                  'municipio', 'colonia', 'calle', 'numero_exterior', 'numero_interior', 'cac', 'status_pospago']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fvc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': date.today().isoformat()}, format='%Y-%m-%d'),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'colonia': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'calle': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'numero_exterior': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'numero_interior': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'cac': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase()'},),
            'status_pospago': forms.Select(attrs={'class': 'form-control'}),
        }

# Funcion para ocultar status

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        rol_activo = kwargs.pop('rol_activo', None)
        super(VentaPospagoForm, self).__init__(*args, **kwargs)

        # Definimos roles
        if rol_activo == 'vendedor':
            es_supervisor = False
        else:
            es_supervisor = user.groups.filter(
                name='SUPERVISORES').exists() or user.is_superuser

        # Por defecto ocultamos el campo status_pospago
        self.fields['status_pospago'].widget = forms.HiddenInput()
        self.fields['status_pospago'].label = ""

        # Si es Supervisor (o Admin), habilitamos el campo status_pospago
        if es_supervisor:
            self.fields['status_pospago'].widget = forms.Select()
            self.fields['status_pospago'].label = "Status Pospago"

# Validacion para que los datos nombre, apellidos y curp se guarden en mayusculas para pospago

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

    def clean_rfc(self):
        return self.cleaned_data.get('rfc', '').upper()

    def clean_identificacion(self):
        return self.cleaned_data.get('identificacion', '').upper()

    def clean_email(self):
        return self.cleaned_data.get('email', '').upper()

    def clean_municipio(self):
        return self.cleaned_data.get('municipio', '').upper()

    def clean_colonia(self):
        return self.cleaned_data.get('colonia', '').upper()

    def clean_calle(self):
        return self.cleaned_data.get('calle', '').upper()
