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

from PyQt5 import QtWidgets, uic, QtCore
import sys
from scrapy import Scrap
from datetime import datetime
from save import save

_ver = '0.3b'


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi('main.ui', self) # Load the .ui file
        self.setWindowTitle('MIOScraper {}'.format(_ver))

        self.scrapy_init()
        self.show()  # Show the GUI
        self.scrap = Scrap()

    def scrapy_init(self):
        self.file_name = None
        self.adr_ip = '172.16.172.66'
        self.connect_status = False

        self.connect_button = self.findChild(QtWidgets.QPushButton, 'connect_btn')
        self.connect_button.clicked.connect(self.connect)

        self.scrap_button = self.findChild(QtWidgets.QPushButton, 'scrap_btn')
        self.scrap_button.clicked.connect(self.scrap)

        self.file_adr_line = self.findChild(QtWidgets.QLineEdit, 'file_adr')

        self.comboBox_ip = self.findChild(QtWidgets.QComboBox, 'comboBox_ip')
        self.comboBox_ip.currentIndexChanged.connect(self.box_ip)

        self.log_box = self.findChild(QtWidgets.QPlainTextEdit, 'log_box')

    def connect(self):
        self.connect_status, log = self.scrap.connect(self.adr_ip)
        self.log(log)

        if self.connect_status:
            self.scrap_button.setEnabled(True)

    def scrap(self):
        log, data_to_save = self.scrap.scrap()
        self.log(log)

        if self.connect_status:
            log = save(self.file_adr_line.text(), data_to_save)
            self.log(log)
            self.connect_status = False
            self.scrap_button.setEnabled(False)
        else :
            log = 'Coś poszło nie tak ...'
            self.log(log)

    def box_ip(self):
        self.adr_ip = self.comboBox_ip.currentText()
        self.log(self.comboBox_ip.currentText())

    def log(self, txt):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        self.log_box.appendPlainText("[{}]:\n{}".format(dt_string, str(txt)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_() # Start