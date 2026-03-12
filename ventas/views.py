from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def prepago(request):
    return render(request, 'prepago.html')

def pospago(request):
    return render(request, 'pospago.html')

def tarjetas(request):
    return render(request, 'tarjetas.html') 
