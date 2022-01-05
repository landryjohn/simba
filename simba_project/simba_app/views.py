import subprocess
from django.contrib.auth.backends import UserModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from simba_app.scripts.scripts import shell_command, SCRIPT_PATH, SUPPORTED_METHOD_LIST

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

@api_view(['POST'])
def system_call(request):
    method = request.POST.get('method', '')
    if method :
        if method not in SUPPORTED_METHOD_LIST : 
            return Response(data={'message':f"{method} method is not supported !"}, status=status.HTTP_200_OK)
        output = subprocess.run(f"python3 {SCRIPT_PATH} -s {method}".split(), capture_output=True, text=True).stdout
        return Response(data={'message':output}, status=status.HTTP_200_OK)
    else:
        return Response(data={'message':'You have to provide a method function'}, status=status.HTTP_200_OK)