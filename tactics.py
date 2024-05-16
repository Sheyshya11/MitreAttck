import json
import requests
from bs4 import BeautifulSoup


# link to website
web_link = "https://attack.mitre.org/tactics/enterprise/"

# get html document
html = requests.get(web_link).text
soup = BeautifulSoup(html, 'html.parser')
table_body = soup.find('table').find('tbody')


# store data in dict
tactics = []

for row in table_body.find_all('tr'):
    tactic = {}
    td_tags = row.find_all('td')
    tactic['tacticsId'] = td_tags[0].find('a').text.strip()
    tactic['tacticsName'] = td_tags[1].find('a').text.strip()
    tactic['tacticsDescription'] = td_tags[2].text.strip()
    tactic['url'] = "https://attack.mitre.org" + td_tags[1].find('a').get('href') 
    tactics.append(tactic)
    # gets all the classes that tr has inside tbody i.e. 'technique' and 'sub technique'
   


# Store the techniques in a dictionary
data_dict = tactics


json_file = open("tactics.json", "w")
json_file.write(json.dumps(data_dict, indent=4))
json_file.close()