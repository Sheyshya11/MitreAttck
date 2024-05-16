import json
import requests
from bs4 import BeautifulSoup


# link to website
web_link = "https://attack.mitre.org/groups/"

# get html document
html = requests.get(web_link).text
soup = BeautifulSoup(html, 'html.parser')
table_body = soup.find('table').find('tbody')


# store data in dict
groups = []

for row in table_body.find_all('tr'):
    group = {}
    td_tags = row.find_all('td')
    group['groupId'] = td_tags[0].find('a').text.strip()
    group['groupName'] = td_tags[1].find('a').text.strip()
    # group['groupDescription'] = td_tags[2].text.strip()
    group['groupDescription'] = "https://attack.mitre.org" + td_tags[1].find('a').get('href') 
    groups.append(group)
    # gets all the classes that tr has inside tbody i.e. 'technique' and 'sub technique'
   


# Store the techniques in a dictionary
data_dict = groups


json_file = open("groups.json", "w")
json_file.write(json.dumps(data_dict, indent=4))
json_file.close()