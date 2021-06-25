from bs4 import BeautifulSoup
import requests
import urllib
import re

site = urllib.request.urlopen('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/#requirementstext')
siteHtml = site.read()

soup = BeautifulSoup(siteHtml, 'html.parser')
require = soup.find(class_ = 'sc_courselist')
#print(require.get_text())
rString = require.get_text().replace(u'\xa0', u' ')

def rebuild_course(res) -> list:
    department = re.match(r"(?:[A-Z&]+\s?[A-Z&]+)+", res)[0]
    

def convert_requirements (req) :
    splitReq = re.split(r"[A-Z]-?[0-9]?\.", req)
    for x in splitReq:
        x = x.strip().strip("\n")
        if ('Upper-division' == x or 'Lower-division'== x or "Specialization" in x):
            continue
        titleReq = re.match(r"(?:.*:\s.*\.|:)|(?:.*:)|(?:.*\.)|(?:[A-Z][a-z]+)", x)
        print(titleReq[0])
        if ('Select' and 'series' in x) :
            series = x.split('or')
            for serie in series:
                # stripped = re.sub(r"\(?[A-Za-z][a-z]+:?\)?", "", serie).strip()
                # print(stripped)
                # rebuild_course(stripped)
                pass
        else:
            pass
            #print(x)
            
            # print(x)
        print()

        
print(convert_requirements(rString))

# Regex for catching course IDS (?:[A-Z&]+\s?[A-Z&]?)+\s(?:[0-9]+[A-Z]*(?:-\s)?)+