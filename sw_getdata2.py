import requests
import json


def fetch_all_characters():
    char_url = 'https://swapi.dev/api/people/'
    # List to store all characters
    all_chars = []
    next_page_url = char_url
    while next_page_url:
        response = requests.get(next_page_url)
        try:
            data = response.json()
            all_chars.extend(data['results'])
            next_page_url = data['next']
        except requests.exceptions.RequestException as e:
            print(f'Failed to fetch data from SWAPI (status code: {e})')
            break

    return all_chars


def extract_character_info(character):
    # pull data into local app
    character_data = {
        'name': character['name'],
        'hair_color': character['hair_color']
    }

    # Fetch and include homeworld name
    homeworld_url = character['homeworld']
    homeworld_response = requests.get(homeworld_url)
    if homeworld_response.status_code == 200:
        homeworld_data = homeworld_response.json()
        character_data['homeworld'] = homeworld_data['name']
    else:
        character_data['homeworld'] = "Unknown"

    # Fetch and include species name(s)
    species_urls = character['species']
    species_names = []
    for species_url in species_urls:
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            species_data = species_response.json()
            species_names.append(species_data['name'])
        else:
            species_names.append("Unknown")
    character_data['species'] = species_names

    return character_data


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


all_chars = fetch_all_characters()

# Extract the selected fields for each character
characters_data = [extract_character_info(character) for character in all_chars]

# Save the data to a JSON file
save_to_json(characters_data, 'swapi_characters2.json')

print('Data saved to swapi_characters2.json')
