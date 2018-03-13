import requests
payload = {
	'username': 'ly',
	'password': '1234'
} # form-data

headers = {
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
} # headers
r = requests.post('http://localhost:88/cs1701/nodejs/day2/login.php', data=payload, headers=headers)
print(r.content)