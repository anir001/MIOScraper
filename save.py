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

from pathlib import Path
import csv
import os
import re


def save(file_name, data):
    valid = '^[\w\-. ]+$'
    if re.match(valid, file_name):
        name = file_name + ".csv"
        path = os.path.join(os.getcwd(), 'output', name)

        with open(path, 'a', newline='', encoding="utf-8") as csvfile:
            save = csv.writer(csvfile, delimiter=';')
            save.writerows(data)
            csvfile.close()

            log = 'Zapisano w {}'.format(path)
        return log

    else:
        log = 'Niepoprawna nazwa pliku, spróbuj jeszcze raz.'
        return log

