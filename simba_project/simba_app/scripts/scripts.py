import subprocess, argparse

SCRIPT_PATH = "/home/mdiai/Desktop/simba/simba_project/simba_app/scripts/scripts.py"
SUPPORTED_METHOD_LIST = [
    'get_intrusion_report',
    'get_signature_database',
    'show_simba_rules',
    'show_services_status',
    'add_block_user_rule',
    'show_firewall_status'
]

def shell_command(array_command) -> None:
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

# show services status 
def show_services_status() -> None : 
    shell_command("sudo service --status-all".split())

# Add block user rule in the firewall
def add_block_user_rule(host_ip_address:str) -> None : 
    # shell_command(f"sudo ufw reject from {host_ip_address} to any".split())
    print("rule added !")

# Show firewall status
def show_firewall_status() -> None : 
    shell_command(f"sudo ufw status".split())

def main():
    parser = argparse.ArgumentParser()

    #Adding switches 
    parser.add_argument('-s', '--script', metavar='', type=str, help='Name of the script to run')
    parser.add_argument('-d', '--payload', metavar='', type=str, help='Payload data')

    args = parser.parse_args()
    
    if args.script == "get_intrusion_report" : 
        get_intrusion_report()
    if args.script == "get_signature_database" :
        get_signature_database()
    if args.script == "show_simba_rules" :
        show_simba_rules() 
    if args.script == "show_services_status" :
        show_services_status() 
    if args.script == "add_block_user_rule" :
        payload = args.payload
        if payload == 'null' : 
            print("[X] payload parameter is required...")
        add_block_user_rule(payload.split(':')[1])
        show_firewall_status()
if __name__ == '__main__':
    main()
