from django.shortcuts import render

def index(request):
    return render(request,'accueil.html')

def searchdb(request):
    return render(request, 'searchdb.html')