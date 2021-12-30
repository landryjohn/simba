from django.shortcuts import render

def index(request): 
    return render(request, 'simba_app/login.html')