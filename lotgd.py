'''
IN FIGHT:
If level 1 and enemy level 2: Run

IN FOREST:
If experience == blue: Level up
If (health < 50%) or (health < 100% and level == 1): Heal
If level 1: Search
If level 2: Thrillseeking
If level > 2: Suicidal
'''

import requests
from bs4 import BeautifulSoup

class Bot:

    village_priority = ["forest"]
    forest_priority = ["search", "fight", "give", "wait", "play", "return",
                "swing", "take", "no", "chicken", "ignoreferryman", "back",
                "nodrink", "leave", "leavestonehenge", "dontplay", "pre"]
    location_priority = ["forest", "village", "news"]
    data_watch = ["Level", "Hitpoints", "Soulpoints"]
    user_agent = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel \
        Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/63.0.3239.132 Safari/537.36' }

    level_up_cue = '<td width="100%" bgcolor="blue">'
    
    domain = None
    cookies = None
    session = None
    payload = None
    current_link = None
    dump = None
    soup = None
    char_info = None
    links = None
    response = None

    # op=search type=thrill type=suicide

    def __init__(self):
        self.domain = "http://www.lotgd.net/"
        self.session = requests.Session()
        
        file = open("login.txt", "r")
        user = file.readline().strip('\n')
        password = file.readline().strip('\n')

        self.payload = {'name' : user, 'password' : password}
        # payload = {'name' : 'PyBot', 'password' : 'PumpkinEater'}

    def find_op(self, op_string):
        for link in links:
            pass
        
    def fight(self):
        if get_level == 1 and get_enemy_level > 1:
            pass
        if get_health() > 0.5:
            pass
    
    # Given a BeautifulSoup soup object, return list of links
    def make_menu(self):
        links = list()
        
        for link in self.soup.findAll('a'):
            if(".php" in link.get('href')):
                links.append(link.get('href'))
                
        return links

    # Creates a dict with essential character info
    def get_char_info(self):
        data = []
        
        charinfo = dict()
        
        charinfo['level'] = 1
        charinfo['health'] = 0
        charinfo['fights'] = 100
        charinfo['gold'] = 100
        charinfo['experience'] = False
        
        
        try:
            table = self.soup.find_all('table')[7] # All tables to right panel
            table = table.find_all('table')[0] # Right panel to charinfo
            table = table.find_all('tr') # Charinfo to charinfo rows
            
            charinfo['level'] = int(table[2].find_all('td')[1].text)
            hp_arr = table[3].find_all('td')[1].text.split('/')
            charinfo['health'] = round(100 * float(hp_arr[0]) / float(hp_arr[1])) / 100
            charinfo['fights'] = int(table[5].find_all('td')[1].text)
            charinfo['gold'] = int(table[11].find_all('td')[1].text)
            charinfo['experience'] = "blue" in str(table[13].find_all('td')[1])
            # charinfo['buffs'] = table[23].find('td').text
        except:
            print("Error when parsing table")
        
        return charinfo
        
    # Given a menu and a priority of commands, picks highest
    def pick_op_priority(self):
        for link in self.links:
            for item in self.forest_priority:
                if("op=" + item in link): # "op=" + item in link
                    return link
                    
    def pick_fight(self):
        if(self.char_info['level'] == 1):
            self.nav_link_with("search")
        elif(1 < self.char_info['level'] < 4):
            self.nav_link_with("thrill")
        else:
            self.nav_link_with("suicide")
                    
    def pick_loc_priority(self):
        for link in self.links:
            for item in self.location_priority:
                if(item + ".php" in link):
                    return link
                    
    # Call pick_option with imprecise substring
    def nav_link_with(self, target):
        for link in self.links:
            if(target in link):
                self.pick_option(link)
                return 0
        return -1
        
    # Navigates to link and returns response, updates all member variables
    def pick_option(self, link):
        print("Navigating to " + link)
        self.current_link = self.domain + link
        self.response = self.session.post(self.current_link, cookies=self.cookies, headers=self.user_agent)
        
        self.update_info()
    
    # Returns True if option exists within link
    def option_exists(self, option):
        for link in self.links:
            if(option in link):
                return True
        return False
        
    def update_info(self):
        self.dump = str(self.response.content)
        # Handle with options other than forest?
        if("Click here." in self.dump):
            self.pick_option("forest.php?")
            return
        
        self.soup = BeautifulSoup(self.dump, features="html.parser")
        self.char_info = self.get_char_info()
        self.links = self.make_menu()
    
    # Begin play session
    def play(self):
        self.current_link = self.domain + "login.php"
        
        self.response = self.session.post(self.domain + "login.php", data=self.payload, headers=self.user_agent)
        self.cookies = self.session.cookies
        self.update_info()

        while(True):
            print(self.char_info)
            # input("Press [ENTER] to continue ")
            
            if(self.char_info['fights'] == 0):
                return
            
            if("healer.php" in self.current_link):
                response_error = self.nav_link_with("pct=100")
                if(response_error == -1):
                    response_error = self.nav_link_with("forest.php")
            elif(self.char_info['experience'] and self.option_exists("village.php")):
                print("Attempting to level up")
                self.nav_link_with("village.php")
                self.nav_link_with("train.php")
                self.nav_link_with("challenge")
                self.nav_link_with("full")
            elif("forest.php" in self.current_link):
                if(self.char_info['health'] < 0.66 and self.option_exists("healer.php")):
                    print("Attempting to heal")
                    self.nav_link_with("healer.php")
                else:
                    if(self.option_exists("search")):
                        self.pick_fight()
                    else:
                        link = self.pick_op_priority()
                        self.pick_option(link)
                '''
                if("Health" in chardata.keys() and chardata["Health"] < 0.5):
                    response = self.nav_link_with(links, "healer.php")
                    if(response == -1):
                        link = self.pick_op_priority(links)
                        response = self.pick_option(link)
                # For fighting in forest
                else:
                '''

            # For navigating to forest
            else:
                link = self.pick_loc_priority()
                self.pick_option(link)
        

    # CURRENTLY UNUSED
    def nav_and_fetch(self):
        response = session.post(domain + "login.php", data=payload, headers=self.user_agent)
        cookies = session.cookies

        dump = str(response.content)
        soup = BeautifulSoup(dump, features="html.parser")
        links = list()

        for link in soup.findAll('a'):
            if(".php" in link.get('href')):
                links.append(link.get('href'))
            if("forest" in link.get('href')):
                response = session.post(domain + link.get('href'), cookies=cookies, headers=self.user_agent)
                print(response.content)
    
bot = Bot()
bot.play()

# print(links)

# print(session.cookies)

# print(str(response.content))
