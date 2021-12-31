from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request): 
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    return render(request, 'simba_app/index.html')