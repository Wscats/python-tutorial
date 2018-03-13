import requests
r = requests.get('http://localhost:88/cq1701/python/python-tutorial/scrapy/test.txt')
print(r.content)
with open("download.txt", "wb") as file:
   file.write(r.content)