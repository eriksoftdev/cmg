from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NotaForm
from .models import Nota
from django.contrib import messages

# Create your views here.
@login_required
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
            messages.success(request, '¡Nota creada con éxito!')
            return redirect('notas')
        else:
            messages.error(request, '¡Error al crear la nota!')
            return redirect('notas')
        

@login_required
def update_note(request, note_id):
    note = get_object_or_404(Nota, id=note_id, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.description = request.POST.get('description')
        note.save()
        messages.success(request, '¡Nota actualizada correctamente!')
        return redirect('notas')
    return redirect('notas')

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Nota, id=note_id, user=request.user)
    note.delete()
    messages.success(request, '¡Nota eliminada!')
    return redirect('notas')