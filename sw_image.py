import requests
from bs4 import BeautifulSoup
from sw_game import character_name


def search_sw_img():
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
            print('Second image URL:', second_image_url)
        else:
            print('Not enough images found in the search results')
    else:
        print(f'Failed to fetch images from search engine (status code: {response.status_code})')
