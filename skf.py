import requests 
from colorama import Fore, Style
import json
import re
import argparse
"""
Project_main_author: @blabla1337 (Github)
project_name: Security Knowledge Framework
project_description: A tool to help security researchers and security engineers to learn and understand security concepts.
CLI Version Author: @joyghoshs (Github)
CLI Version Name: Security Knowledge Framework CLI
CLI Version Description: A CLI version of the Security Knowledge Framework
"""
def logo():
    print(f"""      
{Fore.GREEN}
    ╔═╗╦╔═╔═╗  ╔═╗╦  ╦
    ╚═╗╠╩╗╠╣───║  ║  ║
    ╚═╝╩ ╩╚    ╚═╝╩═╝╩ {Fore.RED}@0xjoyghosh{Style.RESET_ALL}
   ----------------------
Security Knowledge Framework  {Fore.RED}@blabla1337{Style.RESET_ALL}
    """)

logo()
def stop_lab(user, lab):
    url = "https://demo.securityknowledgeframework.org:443/api/interactive_labs/delete-deployments/"+lab
    user_agent = {'User-Agent': 'Chrome/81.0.4044.138'}
    payload = {"user_id": user}
    resp = requests.request("POST", url, json=payload, headers=user_agent)
    print(f"[{Fore.RED}STOP{Style.RESET_ALL}] {Fore.BLUE}Lab Stopped{Style.RESET_ALL}")
def start_lab(user, lab, lab_name, writeup):
    print(f"[ {Fore.GREEN}LAB{Style.RESET_ALL} ] {Fore.GREEN}Starting {lab_name} lab{Style.RESET_ALL}")
    url = "https://demo.securityknowledgeframework.org:443/api/interactive_labs/deployments/"+lab
    user_agent = {'User-Agent': 'Chrome/81.0.4044.138'}
    payload = {"user_id": user}
    resp = requests.request("POST", url, json=payload, headers=user_agent)
    lab = re.search(r'https://(.*?)\.securityknowledgeframework-labs.org', resp.text).group(1)
    lab = f"https://{lab}.securityknowledgeframework-labs.org"
    print(f"[ {Fore.GREEN}LAB{Style.RESET_ALL} ] {Fore.WHITE}{lab}{Style.RESET_ALL}")
    input(f"[ {Fore.YELLOW}WARNING{Style.RESET_ALL} ] Press Any Key to Show the Writeup {Style.RESET_ALL}")
    print(f"[ {Fore.GREEN}WRITEUP{Fore.RESET} ] {writeup}")
    input(f"[ {Fore.YELLOW}WARNING{Style.RESET_ALL} ] Press Any Key to Stop Lab")
    stop_lab(user, lab)
def lab_items():
    api = "https://demo.securityknowledgeframework.org/api/interactive_labs/items"
    user_agent = {'User-Agent': 'Chrome/81.0.4044.138'}
    req = requests.get(api, headers=user_agent)
    data = json.loads(req.text)
    data = data['items']
    return data
def search_lab(user, query):
    data = lab_items()
    print(f"[ {Fore.YELLOW}QUERY{Style.RESET_ALL} ] Searching for {Fore.GREEN}{query}{Style.RESET_ALL}")
    for item in data:
        if query in item['title']:
            print(f"[ {Fore.BLUE}LAB ID: {Fore.RED}{item['id']}{Style.RESET_ALL} ] {Fore.GREEN}{item['title']}{Style.RESET_ALL}")
            option = input(f"[ {Fore.YELLOW}OPTION{Style.RESET_ALL} ] {Fore.WHITE}Do you want to start the Lab {item['id']} (Y/N)? {Style.RESET_ALL}")
            if option == "Y":
                start_lab(user, str(item['id']), item['title'], item['link'])
            else:
                pass
        else:
            pass
def show_labs():
    data = lab_items()
    for item in data:
        print(f"[ {Fore.BLUE}LAB ID: {Fore.RED}{item['id']}{Style.RESET_ALL} ] {Fore.GREEN}{item['title']}{Style.RESET_ALL}")
def writeup(id):
    data = lab_items()
    id = int(id)
    for item in data:
        if id == item['id']:
           return item['link']

def title(id):
    data = lab_items()
    id = int(id)
    for item in data:
        if id == item['id']:
           return item['title']

try:
    parser = argparse.ArgumentParser(description="Security Knowledge Framework CLI")
    parser.add_argument("-u", "--user", help="User ID", required=False, default="system00-sec")
    parser.add_argument("-l", "--lab", help="Lab ID", required=False)
    parser.add_argument("-s", "--search", help="Search for a lab", required=False)
    parser.add_argument("-sh", "--show", help="Show all labs", required=False)
    args = parser.parse_args()
    if args.lab:
        start_lab(args.user, args.lab, title(args.lab), writeup(args.lab))
    elif args.search:
        search_lab(args.user, args.search)
    elif args.show:
        show_labs()
    else:
        print(f"[ {Fore.YELLOW}ERROR{Style.RESET_ALL} ] {Fore.RED}Please specify a lab or search term{Style.RESET_ALL}")
except Exception as e:
    print(f"[ {Fore.YELLOW}ERROR{Style.RESET_ALL} ] {Fore.RED}{e}{Style.RESET_ALL}")
    exit()
except KeyboardInterrupt:
    print(f"\n[ {Fore.YELLOW}EXIT{Style.RESET_ALL} ]")
    exit()
except:
    pass
    exit()
