import pathlib

from bs4 import BeautifulSoup
import requests

import web_utils

REGION = '5E219'

def download_soup(page_path:str, page_type:str, region_key:str, index_key:str):
    page = requests.get(page_path)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open(f"./{page_type}_folder/{region_key}_{index_key}.html", "w") as file:
        file.write(str(soup))

def load_soup(page_type:str, region_key:str, index_key:str):
    with open(f'./{page_type}_folder/{region_key}_{index_key}.html') as fp:
        return BeautifulSoup(fp, 'html.parser')

## First, let's write a script to download a page from rightmove and save it locally

'''pathlib.Path('query_folder').mkdir(exist_ok=True, parents=True)
page_path = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219&index=0"

download_soup(page_path, 'query', REGION, f'1')'''

## Then, we load a soup and analyse it to get the list of properties
'''query_soup = load_soup('query', region_key=REGION, index_key='0')

properties_links = query_soup.find_all("a", {'class':"propertyCard-link" ,'data-test':"property-details"})

for hyper_ref in properties_links:
    property_data = web_utils.get_property_data(property_key=f"https://www.rightmove.co.uk{hyper_ref.get('href')}")
    print(f"Processing property id {property_data['id']}")
    for key, value in property_data.items():
        print(key, value)'''