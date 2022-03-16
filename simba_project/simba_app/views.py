import datetime
import json
import re
import subprocess, requests
from django.http import HttpResponse
from django.contrib.auth.backends import UserModel
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser 

from simba_app.scripts.scripts import shell_command, SCRIPT_PATH, SUPPORTED_METHOD_LIST

# from simba_app.dlmodel import brain

from random import choice

import environ


# Initialise environment variables
env = environ.Env()

# TODO : remove the test view 
def test(request):
    BASE_URL = "http://192.168.8.30:9000"
    data = {}
    # get_intrusion_report
    data['result'] = requests.post(f"{BASE_URL}/api/system_call/", data={'method':'get_intrusion_report'}).json()['message'].replace('\n', '<br>')
    alerts_number = data['result'].count('Classification')
    if alerts_number : 
        today = f"{datetime.datetime.now():%d-%m-%Y}"
        flow_list = re.findall(' .* ->', data['result'])
        print('flow_list', flow_list)
        attackers = set([ machines.split()[-2] for machines in flow_list ])
        print('attackers', attackers)
        data['bot_answer'] = f"Je détecte actuellement {alerts_number} alertes dans le système de détection des intrusions pour la journée du {today.replace('-',' ')}. "
        data['bot_answer'] += f"Les machines suspectent dans le réseau 192.168.8.0/24 sont les suivantes : "
        data['bot_answer'] += f"{' '.join(attackers)}"
    else : 
        data['bot_answer'] = "Aucune alerte à signaler pour aujourd'hui"
    return HttpResponse(data['bot_answer'])

def index(request): 
    if request.user.is_authenticated :
        return redirect('simba_app:login')
    else :
        return redirect('simba_app:home')

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
@authentication_classes([])
@permission_classes([])
def system_call(request):
    method = request.POST.get('method', '')
    payload = request.POST.get('payload', 'null')
    if method :
        if method not in SUPPORTED_METHOD_LIST : 
            return Response(data={'message':f"{method} method is not supported !"}, status=status.HTTP_200_OK)
        output = subprocess.run(f"python3 {SCRIPT_PATH} -s {method} -d {payload}".split(), capture_output=True, text=True).stdout
        return Response(data={'message':output}, status=status.HTTP_200_OK)
    else:
        return Response(data={'message':'You have to provide a method function'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def prediction(request):
    # Set this to the ip address of the application server
    BASE_URL = "http://192.168.8.30:9000"
    command = request.data.get('command', None)
    AI_SCRIPT_PATH = "/home/mdiai/Desktop/simba/simba_project/simba_app/scripts/ai.py"
    with open('/home/mdiai/Desktop/simba/simba_project/simba_app/scripts/command.txt', 'w') as command_file:
        command_file.write(command)
    # intents = brain.class_prediction(command.lower(), brain.words, brain.classes)
    # intent = brain.get_intent(intents, brain.data)
    output = subprocess.run(f"python3 {AI_SCRIPT_PATH}".split(), capture_output=True, text=True).stdout
    intent = dict(json.loads(output))
    data = {}
    data['bot_answer'] = choice(intent["responses"])
    data['tag'] = intent["tag"] 
    if intent["tag"] == 'grettings' : 
        data['bot_answer'] += " Comment puis-je vous aider" 
    elif intent["tag"] == 'services_status' :
        # show_services_status
        data['result'] = requests.post(f"{BASE_URL}/api/system_call/", data={'method':'show_services_status'}).json()['message'].replace('\n', '<br>')
        data['bot_answer'] = "Voici, le statut de fonctionnement des services dans le serveur de détection d'intrusions" 
    elif intent["tag"] == 'signature_database' : 
        # get_signature_database
        data['result'] = requests.post(f"{BASE_URL}/api/system_call/", data={'method':'get_signature_database'}).json()['message'].replace('\n', '<br>')
        rules_number = data['result'].count('<br>') 
        data['bot_answer'] = f"Il y a actuellement {rules_number} profiles dans la base des signatures d'attaques"
    elif intent["tag"] == 'simba_rules' :
        # show_simba_rules
        data['result'] = requests.post(f"{BASE_URL}/api/system_call/", data={'method':'show_simba_rules'}).json()['message'].replace('\n', '<br>')
        data['bot_answer'] = "Voici les règles personnalisées de MDAIA"
    elif intent["tag"] == 'intrusion_report' : 
        # get_intrusion_report
        intrusion_report = requests.post(f"{BASE_URL}/api/system_call/", data={'method':'get_intrusion_report'}).json()['message']
        data['result'] = intrusion_report.replace('\n', '<br>')
        alerts_number = intrusion_report.count('Classification')
        if alerts_number : 
            today = f"{datetime.datetime.now():%d-%m-%Y}"
            flow_list = re.findall('.* ->', intrusion_report)
            print('flow_list', flow_list)
            attackers = set([ machines.split()[-2] for machines in flow_list ])
            print('attackers', attackers)
            data['bot_answer'] = f"Je détecte actuellement {alerts_number} alertes dans le système de détection des intrusions pour la journée du {today.replace('-',' ')}. "
            data['bot_answer'] += f"Les machines suspectent dans le réseau 192.168.8.0/24 sont les suivantes : "
            data['bot_answer'] += f"{' '.join(attackers)}"
        else : 
            data['bot_answer'] = "Aucune alerte à signaler pour aujourd'hui"
    elif intent["tag"] == 'send_intrusion_report' : 
        # get_intrusion_report via telegram
        BOT_TOKEN = env('TELEGRAM_BOT_KEY')
        CHATID = env('TELEGRAM_CHAT_ID')
        content = f"Rapport du {datetime.datetime.now():%d-%m-%Y}\n\n========================\n\n"
        content += requests.post(f"{BASE_URL}/api/system_call/", data={'method':'get_intrusion_report'}).json()['message']
        if len(content) > 4095:
            for x in range(0, len(content), 4095):
                r = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHATID}&text={content[x:x+4095]}').json()
        else:
            r = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHATID}&text={content}').json()
        # r = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHATID}&text={content}').json()
        if r["ok"] :
            data['bot_answer'] = "Le rapport d'intrusions à été bien envoyé"
        else :
            data['bot_answer'] = "un problème est survenu lors de l'envoi du rapport d'intrusion. Consulter les logs."
    elif intent["tag"] == 'block_user_rule' : 
        # TODO : add logic according to the intent
        data['result'] = "Bloquer un utilisateur"
    elif intent["tag"] == 'add_rule' : 
        # TODO : add logic according to the intent  
        data['result'] = "Ajouter un règle de gestion des intrusions"
    elif intent["tag"] == 'firewall' : 
        # TODO : add logic according to the intent  
        data['result'] = "Afficher la configuration pare-feu"
    elif intent["tag"] == 'red_code' : 
        # TODO : add logic according to the intent  
        data['result'] = "Activation du code rouge"
    elif intent["tag"] == 'ssh_connections' : 
        # TODO : add logic according to the intent  
        data['result'] = "Affichage des dernières connexions SSH"
    elif intent["tag"] == 'stop_simba_client' : 
        # TODO : add logic according to the intent  
        data['result'] = "Stop MDIAI bot"
    return Response(data=data, status=status.HTTP_200_OK)
