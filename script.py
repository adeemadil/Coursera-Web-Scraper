# Importing Libraries
# from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests

# function to extract html document from given url
def getHTMLdocument(url):

    # request for HTML document of given url
    response = requests.get(url)

    # response will be provided in JSON format
    return response.text

#function to Remove non-ASCII characters
def cleanText(temp_roles):
    roles = []
    for role in temp_roles:
        # print(role)
        text = role.get_text().strip()
        res = re.sub(r'[^\x00-\x7F]+',' ', text)
        roles.append( res)
    return roles


# CONSTANTS
URL = 'https://boards.greenhouse.io/embed/job_board?for=coursera'
HTML_DOC = getHTMLdocument(URL)

soup = BeautifulSoup(HTML_DOC, 'html.parser')
urls = []

# Loop to acquire urls of job boards on the Careers page of coursera
for link in soup.find_all('a'):
    urls.append(link.get('href'))
    # print(link.get('href'))
print(urls)

# Sending GET Requests to each url acquired from STEP 1 for each job_board to get the description and details
result = []

for url in urls:

    JOB_ID = urls[0].split('gh_jid=')[1]
    TOKEN = 'https://boards.greenhouse.io/embed/job_app?for=coursera&token=' + str(JOB_ID)
    RES_HTML = getHTMLdocument(TOKEN)


    B_SP = BeautifulSoup(RES_HTML, 'html.parser')

    #Finding Title
    title = B_SP.find('h1', class_='app-title').get_text().strip()

    #Finding Company Name
    company = B_SP.find('span', class_='company-name').get_text().strip().split(" ")[1]

    #Finding Location
    location = B_SP.find('div', class_='location').get_text().strip()

    #Finding Overview of Job
    job_overview = B_SP.select('#content p:nth-of-type(2)')[1].get_text().strip()

    #Finding Responsibilities
    temp_roles = B_SP.select('#content ul:first-of-type li')
    roles = cleanText(temp_roles)

    #Finding Basic Qualifications
    temp_basic_quali = B_SP.select('#content ul:nth-of-type(2) li')
    basic_quali = cleanText(temp_basic_quali)

    #Finding Preffered Qualifications
    temp_pref_quali = B_SP.select('#content ul:nth-of-type(3) li')
    pref_quali = cleanText(temp_pref_quali)

    temp = {'Title': title, 'Company' : company, 'Location': location, 'Job Overview': job_overview,
        'Roles': roles, 'Basic Qualifications': basic_quali, 'Preffered Qualifications': pref_quali}

    result.append(temp)

for item in result:
    # print('Opening:\n', item, '\n')
    for k,v in item.items():
        if( k == 'Roles' or k == 'Basic Qualifications' or k == 'Preffered Qualifications'):
            print(k , ":")
            for list_item in v:
                print(list_item)
            print("\n")
        else:
            print(k, ":\n", v)
            print('\n')
    print('\n')
    