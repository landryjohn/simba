import subprocess, argparse

SCRIPT_PATH = "/home/simba/project-lab/simba/simba_project/simba_app/scripts/scripts.py"
SUPPORTED_METHOD_LIST = [
    'get_intrusion_report', 
    'get_signature_database',
    'show_simba_rules'
]

def shell_command(array_command:list) -> None:
    print(subprocess.run(array_command, capture_output=True, text=True).stdout)

# method to gel all alert of the current day
def get_intrusion_report() -> None:
    shell_command("cat /var/log/snort/alert".split())

# get the list of all rules of the IDS
def get_signature_database() -> None:
    shell_command("ls /etc/snort/rules/".split())

# show simba rules in the IDS
def show_simba_rules() -> None : 
    shell_command("cat /etc/snort/rules/simba.rules".split())

def main():
    parser = argparse.ArgumentParser()

    #Adding switches 
    parser.add_argument('-s', '--script', metavar='', type=str, help='Name of the script to run')

    args = parser.parse_args()
    
    if args.script == "get_intrusion_report" : 
        get_intrusion_report()
    if args.script == "get_signature_database" :
        get_signature_database()
    if args.script == "show_simba_rules" :
        show_simba_rules() 
      
if __name__ == '__main__':
    main()
