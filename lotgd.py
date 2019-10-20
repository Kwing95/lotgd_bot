import requests
from bs4 import BeautifulSoup

domain = "http://www.lotgd.net/"
session = requests.Session()
payload = {'name' : 'usenamehere', 'password' : 'passwordhere'}

response = session.post(domain + "login.php", data=payload)
cookies = session.cookies

dump = str(response.content)
soup = BeautifulSoup(dump, features="html.parser")
links = list()

for link in soup.findAll('a'):
	if(".php" in link.get('href')):
		links.append(link.get('href'))
	if("forest" in link.get('href')):
		response = session.post(domain + link.get('href'), cookies=cookies)
		print(response.content)
	
# print(links)

# print(session.cookies)

# print(str(response.content))
