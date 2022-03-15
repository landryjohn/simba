import argparse, json

from dlmodel import brain

def ai_engine():
    pass

def main():
    parser = argparse.ArgumentParser()

    #Adding switches 
    parser.add_argument('-c', '--command', metavar='', type=str, help='User command')

    args = parser.parse_args()
    command = ''
    with open('/home/mdiai/Desktop/simba/simba_project/simba_app/scripts/command.txt', 'r') as command_file :
        command = command_file.readline()
    intents = brain.class_prediction(command.lower(), brain.words, brain.classes)
    intent =  brain.get_intent(intents, brain.data)
    print(json.dumps(intent))

if __name__ == '__main__':
    main()
