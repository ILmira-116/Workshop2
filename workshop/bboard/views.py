from django.shortcuts import render

def index(request):
    return render(request, 'bboard/index.html')
# Create your views here.
