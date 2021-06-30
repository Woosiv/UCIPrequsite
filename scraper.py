from bs4 import BeautifulSoup
import requests
import urllib
import re

site = urllib.request.urlopen('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/#requirementstext')
siteHtml = site.read()

soup = BeautifulSoup(siteHtml, 'html.parser')
# Course listing are under the sc_courselist class tag
require = soup.find(class_ = 'sc_courselist')
require2 = soup.find_all(class_ = ['bubblelink code', 'courselistcomment'])
#print(require.get_text())
rString = require.get_text().replace(u'\xa0', u' ')
rString2 = require.get_text().replace(u'\xa0', u' ')

# Using Beautiful Soup to get the requirements instead of regex 
def convert_requirement (req : BeautifulSoup) -> dict:
    res = {}
    last_req = ''
    course = []
    last_depart = ''
    for div in req:
        text = div.get_text().replace(u'\xa0', u' ')
        if 'bubblelink' in div['class']:
            try:
                last_depart = re.match(r"(?:[A-Z&]+[0-9]?\s?[A-Z&]+)+", text)[0]
                course.append(text)
            except:
                course.append(last_depart + text)
            print('Class')
            if div.parent.has_attr('class') and 'orclass' in div.parent['class']:
                temp = []
                temp.append(course)
                course = temp
        elif 'courselistcomment' in div['class']:
            print('Requirement')
            if last_req:
                res[last_req] = course
                last_req = ''
                course = []
            last_req = div.get_text()
            print(last_req)
        print()
    print(res)

convert_requirement(require2)

assert False
# Helper regex that removes title descriptors as well as white spaces
def stripTitle(target : str) -> str:
    return re.sub(r"\(?[A-Za-z][a-z]+:?\)?", "", target).strip()

# Used to rebuild the course codes for series of classes
def rebuild_series(res : str) -> list:
    lst = []
    # Takes the department from the series
    department = re.match(r"(?:[A-Z&]+[0-9]?\s?[A-Z&]+)+", res)[0]
    # Regexes the course codes
    courseCodes = re.findall(r"(?:[0-9]+[A-Z]*)", res)
    for courseCode in courseCodes:
        lst.append(f'{department}{courseCode}')
    print(lst)
    return lst

# Converts html page into a course dataset
def convert_requirements (req : str) :
    splitReq = re.split(r"[A-Z]-?[0-9]?\.", req)
    for x in splitReq:
        x = x.strip().strip("\n")
        if ('Upper-division' == x or 'Lower-division'== x or "Specialization" in x):
            continue
        titleReq = re.match(r"(?:.*:\s.*\.|:)|(?:.*:)|(?:.*\.)|(?:[A-Z][a-z]+)", x)[0]
        print(titleReq)
        x = re.sub(titleReq, "", x, count = 1).strip()
        #print(x)
        # Checks if the course requirement is multiple
        if ('Select' in titleReq) :
            if 'series' in titleReq:
                series = x.split('or')
                for serie in series:
                    stripped = stripTitle(serie)
                    print(stripped)
                    rebuild_series(stripped)
                
        else:
            courses = x.split("    ")
            for course in courses:
                if ' or ' in course:
                    print("Decisions decisions")
                    print()
                else:
                    courseCodes = re.findall(r"(?:[0-9]+[A-Z]*)", course)
                    print(courseCodes)
            print()

        
print(convert_requirements(rString))

# Regex for catching course IDS (?:[A-Z&]+\s?[A-Z&]?)+\s(?:[0-9]+[A-Z]*(?:-\s)?)+