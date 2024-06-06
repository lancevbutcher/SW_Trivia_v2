from flask import Flask, render_template, request, redirect, url_for
import sw_game
import sw_image

app = Flask(__name__)

# Load character data from JSON files
sw_easy = sw_game.load_json('sw_easy.json')
sw_mid = sw_game.load_json('sw_mid.json')
swapi_characters2 = sw_game.load_json('swapi_characters2.json')

json_files = {
    'sw_easy': sw_easy,
    'sw_mid': sw_mid,
    'swapi_characters2': swapi_characters2
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_file = request.form.get('json-dropdown')
        selected_attribute = request.form.get('attribute-dropdown')
        if selected_file in json_files:
            return redirect(url_for('display_data', filename=selected_file, attribute=selected_attribute))
    return render_template('main.html')


@app.route('/data/<filename>')
def display_data(filename):
    if filename in json_files:
        selected_data = json_files[filename]
        random_character = sw_game.get_random_character(selected_data)
        character_details = sw_game.get_character_details(random_character)
        attribute = request.args.get('attribute', 'homeworld')  # Default to homeworld if not specified
        character_details['attribute'] = attribute
        character_details['filename'] = filename  # Add filename to the context

        # Get image URL
        image_url = sw_image.search_sw_img(character_details['name'])
        character_details['image_url'] = image_url

        return render_template('game.html', **character_details)
    else:
        return "Invalid file name", 404


@app.route('/check_answer/<filename>', methods=['POST'])
def check_answer(filename):
    guess = request.form.get('guess')
    attribute = request.form.get('attribute')
    correct_answer = request.form.get('correct_answer')
    character_name = request.form.get('character_name')

    if guess.lower() == correct_answer.lower():
        result = 'Correct!'
    else:
        result = f'Incorrect!'

    return render_template('result.html', result=result, character_name=character_name, attribute=attribute,
                           homeworld_name=correct_answer,guess=guess)


if __name__ == '__main__':
    app.run(debug=True)
