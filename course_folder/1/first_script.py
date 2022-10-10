## Imports 
# requests is a library that performs requests on websites
import requests
# bs4 is a library that parses (transcripts) requests contents to a readable format
from bs4 import BeautifulSoup
# pathlib is a library that provides an easy way to specify file locations 
import pathlib

## Constants
IMAGE_LINK = 'http://www.bristol.ac.uk/media-library/protected/images/uob-logo-full-colour-largest-2.png'
IMAGE_SAVE_LOCATION = 'bristol_logo.png'
PAGE_LINK  = 'http://www.bristol.ac.uk/economics/'
PAGE_SAVE_LOCATION = 'Bristol_page.html'

## Functions
def save_image(response:requests.Response, save_path:pathlib.Path) -> None:    
    with open(save_path, 'wb') as f:
        f.write(response.content)

def save_webpage(response:requests.Response, save_path:pathlib.Path) -> None: 
    soup = BeautifulSoup(response.content, 'html.parser')   
    with open(save_path, 'w') as f:
        f.write(str(soup))

# Part of the script that does something
image = requests.get(IMAGE_LINK)

save_image(image, IMAGE_SAVE_LOCATION)

page = requests.get(PAGE_LINK)
save_webpage(page, PAGE_SAVE_LOCATION)



