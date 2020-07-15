"""
Copyright 2020 anir001

Ten plik jest częścią MIOScraper.
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

