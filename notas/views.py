from django.shortcuts import render, redirect
from .forms import NotaForm
from .models import Nota

# Create your views here.
def index_notas(request):
    if request.method == 'GET':
        my_notes = Nota.objects.filter(user=request.user).order_by('-created')
        return render(request, 'notas.html', {
        'form': NotaForm(),
        'notes': my_notes
    })
    else:
        form = NotaForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            return redirect('notas')
