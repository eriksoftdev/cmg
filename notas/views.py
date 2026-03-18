from django.shortcuts import render, redirect
from .forms import NotaForm

# Create your views here.
def index_notas(request):
    if request.method == 'GET':
        return render(request, 'notas.html', {
        'form': NotaForm()
    })
    else:
        form = NotaForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            return redirect('notas')
