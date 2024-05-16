import json
import requests
from bs4 import BeautifulSoup


# link to website
web_link = "https://attack.mitre.org/software/"

# get html document
html = requests.get(web_link).text
soup = BeautifulSoup(html, 'html.parser')
table_body = soup.find('table').find('tbody')


# store data in dict
softwares = []

for row in table_body.find_all('tr'):
    software = {}
    td_tags = row.find_all('td')
    software['softwareId'] = td_tags[0].find('a').text.strip()
    software['softwareName'] = td_tags[1].find('a').text.strip()
    # group['groupDescription'] = td_tags[2].text.strip()
    software['description'] = "https://attack.mitre.org" + td_tags[1].find('a').get('href') 
    softwares.append(software)
    # gets all the classes that tr has inside tbody i.e. 'technique' and 'sub technique'
   


# Store the techniques in a dictionary
data_dict = softwares


json_file = open("softwares.json", "w")
json_file.write(json.dumps(data_dict, indent=4))
json_file.close()