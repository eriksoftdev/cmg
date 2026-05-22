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

    class Meta:
        model = VentaPrepago
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'curp', 'dn', 'nip', 'fvc', 'contact1',
                  'contact2', 'email', 'folio', 'usuario_marcador', 'marcador', 'acepta_promo', 'status']
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


# Funcion para ocultar campos de acepta_promo y status

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        rol_activo = kwargs.pop('rol_activo', None)
        super(VentaPrepagoForm, self).__init__(*args, **kwargs)


# Definimos roles
        if rol_activo == 'vendedor':
            es_validador = False
            es_supervisor = False
        else:
            es_validador = user.groups.filter(name='VALIDADORES').exists()
            es_supervisor = user.groups.filter(
                name='SUPERVISORES').exists() or user.is_superuser

        # 1. Por defecto ocultamos ambos
        self.fields['acepta_promo'].widget = forms.HiddenInput()
        self.fields['acepta_promo'].label = ""
        self.fields['status'].widget = forms.HiddenInput()
        self.fields['status'].label = ""

        # 2. Si es Validador o Superior, habilitamos 'acepta_promo'
        if es_validador or es_supervisor:
            self.fields['acepta_promo'].widget = forms.Select(
                choices=[(None, '---'), (True, 'Sí'), (False, 'No')])
            self.fields['acepta_promo'].label = "Acepta Promoción"

        # 3. Solo si es Supervisor (o Admin), habilitamos 'status'
        if es_supervisor:
            # Usa los choices de tu modelo
            self.fields['status'].widget = forms.Select()
            self.fields['status'].label = "Estado de Venta"


# Validacion para que los datos nombre, apellidos y curp se guarden en mayusculas para prepago

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
