from bs4 import BeautifulSoup
import requests
import urllib
import re

site = urllib.request.urlopen('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/')
siteHtml = site.read()

soup = BeautifulSoup(siteHtml, 'html.parser')
# Course listing are under the sc_courselist class tag
require = soup.find(class_ = 'sc_courselist')
require2 = soup.find(id = "requirementstextcontainer").find_all(class_ = ['bubblelink code', 'courselistcomment'])
#print(require.get_text())
rString = require.get_text().replace(u'\xa0', u' ')
rString2 = require.get_text().replace(u'\xa0', u' ')

# Using Beautiful Soup to get the requirements instead of regex 
def convert_requirement (req : BeautifulSoup) -> dict:
    res = {}
    last_req = ''
    last_depart = ''
    course_list = []
    total_course = []
    print(len(req))
    for div in req:
        # print(course_list)
        # print(div)
        text = div.get_text().replace(u'\xa0', u' ')
        # Handles course codes
        if 'bubblelink' in div['class']:
            # Handles or cases within requirements
            if div.parent.has_attr('class') and 'orclass' in div.parent['class']:
                temp = []
                temp.append(course_list.pop())
                temp.append(text)
                total_course.append(temp)
            else:
                try:
                    last_depart = re.match(r"(?:[A-Z&]+[0-9]?\s?[A-Z&]+)+", text)[0]
                    course_list.append(text)
                except:
                    course_list.append(last_depart + text)
        # Handles requirements
        elif 'courselistcomment' in div['class']:
            # If the course list comment is a course
            if re.match(r"(?:[A-Z&]+[0-9]?\s?[A-Z&]+)+", text):
                course_list.append(div.parent.get_text().replace(u'\xa0', u' ').strip())
                continue
            # Handles or requirements between divs
            if ('or' == text):
                total_course.append(course_list)
                course_list = []
                continue

            if len(total_course) == 0:
                total_course = course_list
            elif course_list != total_course:
                total_course.append(course_list)
            
            if last_req:
                #print(last_req)
                res[last_req] = total_course
                last_req = ''
                #print(total_course)
                total_course = []
                course_list = []
            last_req = div.get_text()
            #print(last_req)
        #print()

    # Handles remaining course/reqs
    if course_list:
        if len(total_course) == 0:
            total_course = course_list
        elif course_list != total_course:
            total_course.append(course_list)

    if last_req:
        res[last_req] = total_course
    
    # Output result
    for k,v in res.items():
        print(k)
        print(v)
    
    return res

convert_requirement(require2)

# # Helper regex that removes title descriptors as well as white spaces
# def stripTitle(target : str) -> str:
#     return re.sub(r"\(?[A-Za-z][a-z]+:?\)?", "", target).strip()

# # Used to rebuild the course codes for series of classes
# def rebuild_series(res : str) -> list:
#     lst = []
#     # Takes the department from the series
#     department = re.match(r"(?:[A-Z&]+[0-9]?\s?[A-Z&]+)+", res)[0]
#     # Regexes the course codes
#     courseCodes = re.findall(r"(?:[0-9]+[A-Z]*)", res)
#     for courseCode in courseCodes:
#         lst.append(f'{department}{courseCode}')
#     print(lst)
#     return lst

# # Converts html page into a course dataset
# def convert_requirements (req : str) :
#     splitReq = re.split(r"[A-Z]-?[0-9]?\.", req)
#     for x in splitReq:
#         x = x.strip().strip("\n")
#         if ('Upper-division' == x or 'Lower-division'== x or "Specialization" in x):
#             continue
#         titleReq = re.match(r"(?:.*:\s.*\.|:)|(?:.*:)|(?:.*\.)|(?:[A-Z][a-z]+)", x)[0]
#         print(titleReq)
#         x = re.sub(titleReq, "", x, count = 1).strip()
#         #print(x)
#         # Checks if the course requirement is multiple
#         if ('Select' in titleReq) :
#             if 'series' in titleReq:
#                 series = x.split('or')
#                 for serie in series:
#                     stripped = stripTitle(serie)
#                     print(stripped)
#                     rebuild_series(stripped)
                
#         else:
#             courses = x.split("    ")
#             for course in courses:
#                 if ' or ' in course:
#                     print("Decisions decisions")
#                     print()
#                 else:
#                     courseCodes = re.findall(r"(?:[0-9]+[A-Z]*)", course)
#                     print(courseCodes)
#             print()

        
# print(convert_requirements(rString))

# # Regex for catching course IDS (?:[A-Z&]+\s?[A-Z&]?)+\s(?:[0-9]+[A-Z]*(?:-\s)?)+