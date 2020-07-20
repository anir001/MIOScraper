"""
Copyright 2020 anir001

Ten plik jest częścią MIOScraper.
"""

from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.support.ui import Select

_pattern = '^MIO_select'
_pattern2 = '^javascript'



_name_dict = {'AI8C':'VALD201134L',
            'AI8CN':'VALD201736L',
            'AI8H':'VALD201189L',
            'AI8V':'VALD201135',
            'AII8C':'VALD201473L',
            'AII8CN':'VALD201472L',
            'AII8H':'VALD202388L',
            'AII8V':'VALD201474L',
            'AO4C':'VALD201136L',
            'AO4H':'VALD201190L',
            'AO4V':'VALD201137',
            'AO8C':'VALD202098L',
            'DI8N':'VALD201127L',
            'DI8P':'VALD201126L',
            'DO8N':'VALD201130',
            'DO8P':'VALD201129L',
            'DO8RO':'VALD201131L',
            'DO8SO':'VALD201133',
            'DI8M':'VALD201239L',
            'TI4W3':'VALD201159L',
            'TI4W4':'VALD201171L'}




class Scrap():
    def __init__(self):
        self.url = None
        self.page = None
        self.log = 0
        self.cards_qty = 0
        self.soup = None
        self.table = None
        self.connect_status = False

        self.list_ibc = None
        self.ibc = []
        self.cards_list = []
        self.cards = []
        self.cards_adr = []
        self.adr = None
        self.serials_n = []
        self.sn = 0
        self.card_val = []
        self.driver_state = False


#        """Inicjalizacja selenium"""
#        options = webdriver.ChromeOptions()
#        options.add_argument('--ignore-certificate-errors')
#        options.add_argument('--incognito')
#        #options.add_argument('--headless')
#        self.driver = webdriver.Chrome("chromedriver", chrome_options=options)
    def start_webdriver(self):
        
        """Inicjalizacja selenium"""
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        #options.add_argument('--headless')
        self.driver = webdriver.Chrome("chromedriver", chrome_options=options)
                   
    def get_page(self, url):
        try:

            """test połączenia"""
            requests.get(url, timeout=2)
            """"""
            self.driver.get(url)

            self.page = self.driver.page_source
            self.soup = BeautifulSoup(self.page, 'html.parser')

        except(ConnectionError, Exception) as e:
            self.log = "Coś poszło nie tak:\n{}".format(e)

    def connect(self, url):
        try:
            if not self.driver_state: 
                self.start_webdriver()
                self.driver_state = True
        except :
            print('Przeglądarka nie wystartowała.')        

        self.soup = None
        self.url = url

        self.get_page("http://{}:1269".format(self.url))

        if self.soup is not None:
            self.connect_status = True
            self.log = "Połączono"
        return self.connect_status, self.log

    def get_ibc(self):
        self.table = self.soup.findAll('table')
        self.list_ibc = self.table[0].findAll('option')
        for l in self.list_ibc:

            self.ibc.append(int(l.text))

    def get_card(self):
        self.table = self.soup.findAll('table')
        self.cards = self.table[1].findAll('tr')
        self.cards = self.cards[1].text
        self.cards = self.cards.split()
        self.cards_list += self.cards

    def get_adres(self):
        self.table = self.soup.findAll('table')
        self.adr = self.table[1].findAll('tr')
        self.adr = self.adr[2].findAll('a')
        self.cards_adr.clear()
        for adr in self.adr:

            if re.match(_pattern2, adr.get('href')):  # adres z kart DO/AO
                temp = re.findall(r'\b\d+\b', adr.get('href'))
                self.cards_adr.append('MIO_select.htm?' + str(temp[0]) + '&' + str(temp[1]))

            else:  # adres reszty
                self.cards_adr.append(adr.get('href'))

    def get_sn(self):
        # scrap numerów seryjnych
        self.table = self.soup.findAll('table')
        self.sn = self.table[2].findAll('tr')
        self.sn = self.sn[3].text
        self.sn = self.sn.split(':')
        self.sn = self.sn[1]
        if self.sn is not None:
            self.serials_n.append(self.sn)
        else:
            pass

    def scrap(self, file_name):
        self.cards_adr.clear()
        self.cards_list.clear()
        self.serials_n.clear()
        self.ibc.clear()
        self.get_ibc()
        cab_names = []

        for ibc in range(len(self.ibc)):
            print(f'ibc: {ibc}')
            dropdown = Select(self.driver.find_element_by_id('IBC_number'))
            dropdown.select_by_index(ibc)

            #self.get_page("http://{}:1269/".format(self.url))
            self.get_page(self.driver.current_url)
            self.get_card()
            self.get_adres()

            for c in tqdm(self.cards_adr):
                self.get_page("http://{}:1269/{}".format(self.url, c))
                self.get_sn()
        
        """Zamknięcie Chrome"""
        self.driver.quit()
        self.driver_state = False

        """przygotowanie do zapisu"""

        for c in self.cards_list:
            self.card_val.append(_name_dict[c])
        lenght = len(self.card_val)
        for i in range(lenght):
            cab_names.append(file_name)

        to_save = list(zip(cab_names, self.card_val, self.serials_n, self.cards_list))

        log = "Znaleziono {} kart I/O".format(len(self.serials_n))
        return log, to_save
