import requests

for num in range(0, 101):
    if num % 2!=0:
        html = requests.get(f'http://10.10.114.218/api/{num}')
        print(html.text)
