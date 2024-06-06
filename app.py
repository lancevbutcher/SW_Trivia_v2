from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load character data from JSON file
with open('swapi_characters2.json', 'r') as f:
    characters = json.load(f)


@app.route('/')
def index():
    return render_template('main.html', characters=characters)


@app.route('/api/characters')
def api_characters():
    return jsonify(characters)


if __name__ == '__main__':
    app.run(debug=True)
