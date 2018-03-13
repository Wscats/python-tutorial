import requests
payload = {'name': 'wscats'}
r = requests.get('http://localhost:88/cq1701/python/python-tutorial/scrapy/test.php', params=payload)
print(r.content)