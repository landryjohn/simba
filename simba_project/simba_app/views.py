from django.contrib.auth.backends import UserModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request): 
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    return render(request, 'simba_app/index.html')

@login_required
def users(request):
    users = UserModel.objects.all()
    return render(request, 'simba_app/users.html', {'users':users})

@api_view(['GET'])
def get_users(request):
    return Response({'message':'Hello world'}, status=status.HTTP_200_OK)