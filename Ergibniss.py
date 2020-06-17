#!/usr/bin/env python
# coding: utf-8

import requests
import datetime
from bs4 import BeautifulSoup
import os
#  from urllib.request import urlopen
import re
import time

session = requests.Session()
timeout = time.time()


def get_homepage():
    """Einlogen und Prüfungsverwaltung aufnehmen"""
# Geben Sie die Informationen des "Form", Kundenname&Passport(asdf:"KundenName", fdsa:"Passport")
    kun_info = {'asdf': 'username', 'fdsa': 'Password'}
    login_url = 'https://qisserver.hs-koblenz.de/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm&breadCrumbSource=portal'
    r = session.post(login_url, data=kun_info)

# Prüfungsverwaltung_Seite
    p_v_url = 'https://qisserver.hs-koblenz.de/qisserver/rds?state=change&type=1&moduleParameter=studyPOSMenu&nextdir=change&next=menu.vm&subdir=applications&xml=menu&purge=y&navigationPosition=functions%2CstudyPOSMenu&breadcrumb=studyPOSMenu&topitem=functions&subitem=studyPOSMenu'
    r = session.get(p_v_url)
    return r


def get_nsf_url():
    """Prüfungsan- und -abmeldung & Info über angemeldete Prüfungen &
    Notenspiegel"""

    soup = BeautifulSoup(html_home.text, features='lxml')

    #  URL der Notspiegel Funktionen
    nsf_urls = soup.find_all("a",
                             {'href': re.compile('.*?notenspiegelStudent*')})
    for i in nsf_urls:
        nsf_url = i['href']
    return nsf_url


def get_nt_url():
    """Student Noteseite URL lesen"""
    html_nsf = session.get(nsf_url)
    soup = BeautifulSoup(html_nsf.text, features='lxml')
    #  Noteseite
    nt_urls = soup.find_all("a",
                            {'title': re.compile('Leistung*')})
    for i in nt_urls:
        nt_url = i['href']
    return nt_url


def write_in(inhalt, filename='page.html'):
    """speichen in File, dessen Name mannlich gegeben wird."""
    with open(filename, 'w', encoding='utf-8') as file_objekt:
        file_objekt.write(inhalt)


while True:
    os.system("cls")
# jeder 25 Minuten neu einlogen
    if time.time() >= timeout:
        html_home = get_homepage()
        timeout += 25 * 60
    nsf_url = get_nsf_url()
    html_nt = session.get(get_nt_url())
# Tabelle aufnehmen. Brauchen wir nur die zweite Tabelle, weil die erste Tabelle nur die persionale Informationen enthalt.
    soup = BeautifulSoup(html_nt.text, features='lxml')
    table_nt = soup.find_all('table')[1]
# Die Informationen der Tabelle werden in List gespeichert
    rows = []
    for trs in table_nt.find_all("tr")[1:]:
        cells = []
        for td in trs.find_all("td"):
            cells.append(td.text.strip())
# Die Zeilen von 7000&8000&Titel haben nur 8 Elementen, aber die Zeilen, die wir brauchen, 9 Element haben.
# Zwar man koennte mit Regulaeren Aussruck verteilen, aber das ist Schwer fuer mich. Naechste Mal probiere ich.
        if len(cells) > 8:
            rows.append(cells)

# Bitte geben Sie die Pr.Nummer, die Sie folgen moechten.
    folges = ['11410', '11293', '11311', '11351',
              '11391']
    print('*' * 21)
    print('|'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'|')
    print('*' * 21+"\n"+'-' * 40)
    for folge in folges:
        for row in rows:
            if row[0] == folge:
#                print('*' * 15)
                print(row[1] + '\n' * 2 + row[4] + '\n' * 2 + row[3])
                print('-' * 40)
# Warten 300s(5min) bis naechste Aktualisierung
    time.sleep(300)
#    os.system("cls")
