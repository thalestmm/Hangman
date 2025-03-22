from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'game/index.html')

def deduct(request):
    context = {
        "life": 7
    }
    return render(request, 'game/life.html', context)