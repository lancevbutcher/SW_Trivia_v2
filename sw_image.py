import requests
from bs4 import BeautifulSoup

def search_sw_img(character_name):
    search_query = f'{character_name} Star Wars'
    search_url = f'https://www.google.com/search?q={search_query}&tbm=isch'
    # search for images
    response = requests.get(search_url)
    if response.status_code == 200:
        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        image_elements = soup.find_all('img')
        if len(image_elements) >= 2:
            second_image_url = image_elements[1]['src']
            return second_image_url
        else:
            return None
    else:
        return None
