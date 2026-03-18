from django.forms import ModelForm
from .models import Nota

class NotaForm(ModelForm):
    class Meta:
        model = Nota
        fields = ['title', 'description']