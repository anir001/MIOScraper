"""
To mały krok dla ludzkości, ale dla karła normalny.


Copyright 2020 Deny

Ten plik jest częścią MIOScraper.

MIOScraper jest wolnym oprogramowaniem: możesz go rozprowadzać dalej
i/lub modyfikować na warunkach Powszechnej Licencji Publicznej GNU,
wydanej przez Fundację Wolnego Oprogramowania - według wersji 3 tej
Licencji lub (według twojego wyboru) którejś z późniejszych wersji.

MIOScraper rozpowszechniany jest z nadzieją, iż będzie on
użyteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domyślnej
gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
ZASTOSOWAŃ. W celu uzyskania bliższych informacji sięgnij do     Powszechnej Licencji Publicznej GNU.

Z pewnością wraz z MIOScraper otrzymałeś też egzemplarz
Powszechnej Licencji Publicznej GNU (GNU General Public License).
Jeśli nie - zobacz <http://www.gnu.org/licenses/>.
"""

from bs4 import BeautifulSoup
import requests
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select

_pattern = '^MIO_select'
_pattern2 = '^javascript'


class Scrap:
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


        
        """Inicjalizacja selenium"""
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
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
        print(type(self.sn))
        if self.sn is not None:
            self.serials_n.append(self.sn)
        else:
            pass

    def scrap(self):
        self.cards_adr.clear()
        self.cards_list.clear()
        self.serials_n.clear()
        self.ibc.clear()
        self.get_ibc()
        
        for ibc in range(len(self.ibc)):
            dropdown = Select(self.driver.find_element_by_id('IBC_number'))
            dropdown.select_by_index(ibc)

            #self.get_page("http://{}:1269/".format(self.url))
            self.get_page(self.driver.current_url)
            self.get_card()
            self.get_adres()
            
            for c in self.cards_adr:
                self.get_page("http://{}:1269/{}".format(self.url, c))
                self.get_sn()

        """przygotowanie do zapisu"""
        to_save = list(zip(self.cards_list, self.serials_n))

        log = "Znaleziono {} kart I/O".format(len(self.serials_n))
        return log, to_save

