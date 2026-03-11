from django.shortcuts import render

# Create your views here.
def index_ventas_prepago(request):
    return render(request, 'prepago.html')
def index_ventas_tarjetas(request):
    return render(request, 'tarjetas.html') 

def index_ventas_pospago(request):
    return render(request, 'pospago.html')
