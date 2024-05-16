import json
import requests
from bs4 import BeautifulSoup

# List of website links
website_links = [
    "https://attack.mitre.org/tactics/TA0043/",
    "https://attack.mitre.org/tactics/TA0042/",
     "https://attack.mitre.org/tactics/TA0001/",
      "https://attack.mitre.org/tactics/TA0002/",
       "https://attack.mitre.org/tactics/TA0003/",
        "https://attack.mitre.org/tactics/TA0004/",
         "https://attack.mitre.org/tactics/TA0005/",
          "https://attack.mitre.org/tactics/TA0006/",
           "https://attack.mitre.org/tactics/TA0007/",
            "https://attack.mitre.org/tactics/TA0008/",
             "https://attack.mitre.org/tactics/TA0009/",
              "https://attack.mitre.org/tactics/TA0010/",
               "https://attack.mitre.org/tactics/TA0011/",
                "https://attack.mitre.org/tactics/TA0040/"

    # Add more website links here
]

def scrape_website(web_link, all_data):
    # get html document
    html = requests.get(web_link).text
    soup = BeautifulSoup(html, 'html.parser')
    table_body = soup.find('table', class_='table-techniques').find('tbody')

    cards =  soup.find('div', class_='card-body')
    tactics_id = cards.find_all('div', class_='card-data')[0]
    tactics_name = soup.find('div', class_='container-fluid').find('h1').text.strip()
    tactics= {}
    key = tactics_id.find('span', class_='card-title').text.strip()  # Remove ':' from key
    value = tactics_id.text.strip().replace(key, '')  # Remove the key from the text content
    tactics['id'] = value.strip()

    # store data in dict
    techniques = []
    sub_techniques = []

    for row in table_body.find_all('tr'):
        # gets all the classes that tr has inside tbody i.e. 'technique' and 'sub technique'
        classes = row.get('class', [])
        if 'technique' in classes and 'sub' not in classes:
            # If this is a technique, create a new technique dictionary
            technique = {}

            # Extract technique id, name, and description
            td_tags = row.find_all('td')
            technique['techniquesId'] = td_tags[0].find('a').text.strip()
            technique['techniquesName'] = td_tags[1].find('a').text.strip()
            technique['techniquesDescription'] = td_tags[2].text.strip()
            technique['url'] = "https://attack.mitre.org" + td_tags[1].find('a').get('href') 
            technique['tacticsId'] = tactics['id']
            technique['tacticsName'] = tactics_name

            # Add this technique to the techniques list
            techniques.append(technique)

            # Set the current parent technique
            current_technique = technique

        else:
            # If this is a sub-technique, create a new sub-technique dictionary
            sub_technique = {}

            # Extract sub-technique id, name, and description
            td_tags = row.find_all('td')
            sub_technique['subTechniquesId'] = current_technique['techniquesId'] + td_tags[1].find('a').text.strip()
            sub_technique['techniquesName'] = current_technique['techniquesName']
            sub_technique['subTechniquesName'] = td_tags[2].find('a').text.strip()
            sub_technique['subTechniquesDescription'] = td_tags[3].text.strip()
            sub_technique['url'] = "https://attack.mitre.org" + td_tags[1].find('a').get('href') 
         
            # Add this sub-technique to the current parent technique's "sub-techniques" list
            current_technique.setdefault('sub-techniques', []).append(sub_technique)
            sub_techniques.append(sub_technique)

    # Append the techniques to the existing data
    all_data.extend(sub_techniques)

# Initialize an empty list to store all the technique data
all_data = []

# Iterate over each website link and perform scraping
for link in website_links:
    scrape_website(link, all_data)

# Write all the data to a single JSON file
with open("sub_techniques.json", "w") as json_file:
    json.dump(all_data, json_file, indent=4)
