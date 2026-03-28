from django.forms import ModelForm
from django import forms
from .models import Nota

class NotaForm(ModelForm):
    class Meta:
        model = Nota
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }