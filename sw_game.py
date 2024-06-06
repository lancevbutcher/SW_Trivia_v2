from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
import requests
import random

# Generate a random number between 1 and 82 (the total number of characters in the API)
rand_char_id = random.randint(1, 82)

# Fetch a random character from the Star Wars API
response = requests.get(f'https://swapi.dev/api/people/{rand_char_id}/')
if response.status_code == 200:
    character_data = response.json()
    character_name = character_data['name']
    homeworld_url = character_data['homeworld']

    # Fetch the homeworld details
    homeworld_response = requests.get(homeworld_url)
    if homeworld_response.status_code == 200:
        homeworld_data = homeworld_response.json()
        homeworld_name = homeworld_data['name']

        # Prompt the user to guess the homeworld of the character
        guess = input(f'What is the homeworld of {character_name}? ')

        # Check if the guess matches the correct homeworld
        if guess.lower() == homeworld_name.lower():
            print('Correct!')
        else:
            print(f'Incorrect! The correct homeworld is: {homeworld_name}')
    else:
        print('Failed to fetch homeworld details from API')
else:
    print('Failed to fetch character from API')
