import requests
from bs4 import BeautifulSoup

class Bot:

	village_priority = ["forest"]
	forest_priority = ["search", "fight", "give", "wait", "play", "return", "swing",
				"take", "no", "chicken", "ignoreferryman", "back", "nodrink",
				"leave", "leavestonehenge"]
	location_priority = ["forest", "village", "news"]
	data_watch = ["Level", "Hitpoints", "Soulpoints"]

	level_up_cue = '<td width="100%" bgcolor="blue">'
	
	domain = None
	cookies = None
	session = None
	payload = None
	current_link = None

	# op=search type=thrill type=suicide

	def __init__(self):
		self.domain = "http://www.lotgd.net/"
		self.session = requests.Session()
		
		file = open("login.txt", "r")
		user = file.readline().strip('\n')
		password = file.readline().strip('\n')

		self.payload = {'name' : user, 'password' : password}
		# payload = {'name' : 'PyBot', 'password' : 'PumpkinEater'}

	def find_op(self, links, op_string):
		for link in links:
			pass
		
	def fight(self):
		if get_level == 1 and get_enemy_level > 1:
			pass
		if get_health() > 0.5:
			pass
	
	# Given a BeautifulSoup soup object, return list of links
	def make_menu(self, soup):
		links = list()
		
		for link in soup.findAll('a'):
			if(".php" in link.get('href')):
				links.append(link.get('href'))
				
		return links
		
	# Given a menu and a priority of commands, picks highest
	def pick_op_priority(self, links):
		for link in links:
			for item in self.forest_priority:
				if("op=" + item in link):
					return link
					
	def pick_loc_priority(self, links):
		for link in links:
			for item in self.location_priority:
				if(item + ".php" in link):
					return link
					
	def get_chardata(self, soup):
		chardata = dict()
		
		table = soup.find('table')
		print("table = " + str(type(table)))
		if(type(table) == None):
			return chardata
		table_rows = table.find_all('tr')
		
		# For every row in the table
		for tr in table_rows:
			td = tr.find_all('td')
			if(td[0].text == "Level"):
				chardata["Level"] = int(td[1].text)
			elif(td[0].text == "Hitpoints"):
				hp = (td[1].text).split("/")
				chardata["Health"] = int(hp[0]) / int(hp[1])
			elif(td[0].text == "Soulpoints"):
				hp = (td[1].text).split("/")
				chardata["Health"] = int(hp[0]) / int(hp[1])
			elif(td[0].text == "Experience"):
				chardata["Ready"] = "blue" in str(td[2])
			elif(td[0].text == "Fights"):
				chardata["Fights"] = int(td[1].text)
			
		return chardata
		
	# Navigates to link and returns response
	def pick_option(self, link):
		print("Navigating to " + link)
		self.current_link = self.domain + link
		return self.session.post(self.current_link, cookies=self.cookies)
	
	# Begin play session
	def play(self):
		self.current_link = self.domain + "login.php"
		response = self.session.post(self.domain + "login.php", data=self.payload)
		self.cookies = self.session.cookies

		while(True):
			dump = str(response.content)
			soup = BeautifulSoup(dump, features="html.parser")
			table = soup.find('table')
			table_rows = table.find_all('tr')
			
			chardata = self.get_chardata(soup)
			
			links = self.make_menu(soup)
					
			if("forest.php" in self.current_link):
				link = self.pick_op_priority(links)
				response = self.pick_option(link)
			else:
				link = self.pick_loc_priority(links)
				response = self.pick_option(link)
		
	def nav_and_fetch(self):
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
	
bot = Bot()
bot.play()

# print(links)

# print(session.cookies)

# print(str(response.content))
