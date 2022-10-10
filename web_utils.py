from typing import Dict
from bs4 import BeautifulSoup
import requests
import pathlib
import re
import json
import validators 

def get_page_key(page_link:str) -> str:
    key = 'REGION%(.*)&'
    result = re.search(key, page_link)
    return result.group().split('&')[0].split('%')[1]

def get_page_index(page_link:str) -> str:
    index = '&index=(.*)&'
    result = re.search(index, page_link)
    if result is not None:
        return result.group().split('&')[1][len('index='):]
    else:
        return 0

def get_property_key(property_link:str) -> str:
    key = '/properties/(.*)#'
    result = re.search(key, property_link)
    return result.group().split('/')[-1][:-1]

def get_link_identifier(page_link:str, page_type:str) -> str:
    if page_type == 'query':
        page_id = get_page_key(page_link)
        page_index = get_page_index(page_link)
        return f'{page_id}_{page_index}'
    elif page_type == 'property':
        return get_property_key(page_link)
    else:
        raise ValueError (f'Wrong page_type {page_type} key, must be query or property')

def load_soup(page_identifier:str, page_type:str) -> BeautifulSoup:
    """Loads a soup. If the html is saved locally, loads it. Otherwise, downloads it from the internet. the workflow is as follows:
        - load_soup receives 

    Args:
        page_identifier (str): Can be the id of the page locationCode_indexCode (ex: 5E219_0) OR the url 
        page_type (str): Is it a 'property' page or a 'query' page? 

    Returns:
        BeautifulSoup: the loaded soup
    """
    ## Check wether we receive a valid url
    if validators.url(page_identifier):
        ## If the url is valid, parse it to get its identifier 
        page_identifier = get_link_identifier(page_identifier, page_type)
    ## Instanciate the file path and try to open it. If a FileNotFoundError is raised, download it
    page_file_path = pathlib.Path(f'{page_type}_folder/{page_identifier}.html')
    try:        
        with open(page_file_path) as fp:
            return BeautifulSoup(fp, 'html.parser')
    except FileNotFoundError(f'File path {page_file_path} not found locally, downloading...'):
        try:
            page = requests.get(page_identifier)
            soup = BeautifulSoup(page.content, 'html.parser')
            with open(f"{page_type}_folder/{page_identifier}.html", "w") as file:
                file.write(str(soup))
        except requests.ConnectionError:
            print(f'A connection error has occured, please check the provided link: {page_identifier}')
    return soup

def get_property_data(property_key='85672188') -> Dict:
    """Given the name of a property (its ID key) returns all the dictionnary information from the property

    Args:
        property_key (str, optional): ID key of the property (from RightMove DB). Defaults to '85672188'.

    Returns:
        Dict: A dictionnary with all the information about the property 
    """
    s = load_soup(property_key, 'property')
    scripts = s.find_all('script')
    for script in scripts:
        key = 'window.PAGE_MODEL = (.*)'
        result = re.search(key, str(script))
        if result is not None:
            string_of_interest = result.groups()[0]
            dict_of_interest   = json.loads(string_of_interest)
            property_data = dict_of_interest['propertyData']
            return property_data

def save_image(response:requests.Response, save_path:pathlib.Path):
    """Saves an image

    Args:
        response (requests.Response): The response from a url
        save_path (pathlib.Path): The path to save the data
    """
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)

def download_images(image_type:str, images_dict:dict, property_id):
    """Download Images from a property

    Args:
        image_type (str): type of image (epcgraph..., floorplans...)
        images_dict (dict): Dict containing all image URLS
        property_id (_type_): id of the property to get
    """
    save_path = pathlib.Path(f"images/{property_id}")
    save_path.mkdir(exist_ok=True, parents =True)
    for image_index, image_dict in enumerate(images_dict):
        if 'url' in image_dict and not save_path.joinpath(f'{image_type}_{image_index}.jpg').is_file():
            response = requests.get(image_dict['url'])
            save_image(response, save_path.joinpath(f'{image_type}_{image_index}.jpg'))