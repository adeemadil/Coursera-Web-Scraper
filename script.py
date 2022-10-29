# Importing Libraries
# from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# function to extract html document from given url


def getHTMLdocument(url):

    # request for HTML document of given url
    response = requests.get(url)

    # response will be provided in JSON format
    return response.text


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
    JOB_ID = url.split('gh_jid=')[1]
    TOKEN = 'https://boards.greenhouse.io/embed/job_app?for=coursera&token={JOB_ID}'
    RES_HTML = getHTMLdocument(url)
    B_SP = BeautifulSoup(RES_HTML, 'html.parser')

    title = B_SP.find('h1', class_='app-title')
    company = B_SP.find('span', class_='company-name')
    location = B_SP.find('div', class_='location')
    # job_overview = B_SP.find('')
    # roles = B_SP.find('')
    # basic_quali = B_SP.find('')
    # pref_quali = B_SP.find('')

    temp = {'Title': title, 'Company' : company, 'Location': location, 'Job Overview': job_overview,
        'Roles': roles, 'Basic Qualifications': basic_quali, 'Preffered Qualifications': pref_quali}
    
    result.append(temp)