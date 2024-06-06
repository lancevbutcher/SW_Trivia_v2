import json
import random


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def get_random_character(data):
    return random.choice(data)


def get_character_details(character):
    species = character.get('species', [])
    species_str = ', '.join(species) if species else 'Human'

    return {
        'name': character.get('name', 'Unknown'),
        'homeworld': character.get('homeworld', 'Unknown'),
        'species': species_str
    }
