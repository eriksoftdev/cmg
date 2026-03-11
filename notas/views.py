from django.shortcuts import render

# Create your views here.
def index_notas(request):
    return render(request, 'notas.html')
