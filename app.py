import threading
import time
import signal
import ldclient
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from ldclient.config import Config
from ldclient.context import Context
import sw_game
import sw_image
from concurrent.futures import ThreadPoolExecutor
import user_agents

app = Flask(__name__)
socketio = SocketIO(app)


# Directly include your LaunchDarkly SDK key
sdk_key = "YOUR SDK KEY"


# Check SDK
if not sdk_key:
    raise ValueError("The LaunchDarkly SDK key needs to be set")

# Initialize only once
ldclient.set_config(Config(sdk_key))
client = ldclient.get()


# Load character data from JSON files
sw_easy = sw_game.load_json('sw_easy.json')
sw_mid = sw_game.load_json('sw_mid.json')
swapi_characters2 = sw_game.load_json('swapi_characters2.json')


json_files = {
    'sw_easy': sw_easy,
    'sw_mid': sw_mid,
    'swapi_characters2': swapi_characters2
}

# Define the stop event
stop_event = threading.Event()

def poll_flag_changes():
    print('Polling thread started')
    current_value = client.variation("image-hint", {"key": "browser-type", "name": "browser_name"}, False)
    while not stop_event.is_set():
        time.sleep(5)
        new_value = client.variation("image-hint", {"key": "browser-type", "name": "browser_name"}, False)
        if new_value != current_value:
            print(f"Polling: image-hint has changed from {current_value} to {new_value}")
            socketio.emit('flag_value_update',
                          {'flag_key': "image-hint", 'old_value': current_value, 'new_value': new_value})
            current_value = new_value
    print('Polling thread stopped')


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    stop_event.set()
    raise KeyboardInterrupt


# Register the signal handlers
signal.signal(signal.SIGTERM, service_shutdown)
signal.signal(signal.SIGINT, service_shutdown)

# Start the polling thread using ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=1)
executor.submit(poll_flag_changes)


# Define a listener for general flag changes
def flag_change_listener(flag_change):
    print(f"Websocket: {flag_change.key} has changed")
    socketio.emit('flag_update', {'flag_key': flag_change.key})


# Define a listener for specific flag value changes
def flag_value_change_listener(flag_change):
    print(f"Websocket: {flag_change.key} has changed from {flag_change.old_value} to {flag_change.new_value}")
    socketio.emit('flag_value_update',
                  {'flag_key': flag_change.key, 'old_value': flag_change.old_value, 'new_value': flag_change.new_value})



@app.route('/', methods=['GET', 'POST'])
def index():
    # old -> context = get_user_context()
    user_agent = request.headers.get('User-Agent')
    ua = user_agents.parse(user_agent)
    browser_name = str(ua.browser.family)
    browser_set = Context.builder('browser-final4').name(browser_name).set('name', browser_name).build() # .set('browser_set', browser_name)
    browser_set_dict = browser_set.to_dict()
    show_med_level = client.variation("show-med-level", browser_set_dict, False)
    # Default to False if undefined
    if request.method == 'POST':
        selected_file = request.form.get('json-dropdown')
        selected_attribute = request.form.get('attribute-dropdown')
        if selected_file in json_files:
            return redirect(url_for('display_data', filename=selected_file, attribute=selected_attribute))
    return render_template('main.html', show_med_level=show_med_level)


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

        # Evaluate the image-hint feature flag
        user_agent = request.headers.get('User-Agent')
        ua = user_agents.parse(user_agent)
        browser_name = str(ua.browser.family)
        browser_set = Context.builder('browser-final5').name(browser_name).set('name',
                                                                               browser_name).build()  # .set('browser_set', browser_name)
        browser_set_dict = browser_set.to_dict()
        show_med_level = client.variation("show-med-level", browser_set_dict, False)

        character_details['show_hint'] = show_med_level

        # Create a context for feature evaluation
        # old code -> context = get_user_context()

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
        result = 'Incorrect!'

    return render_template('result.html', result=result, character_name=character_name, attribute=attribute,
                           homeworld_name=correct_answer, guess=guess)


if __name__ == '__main__':
    try:
        socketio.run(app, debug=True)
    except KeyboardInterrupt:
        print("Stopping threads and shutting down gracefully.")
        stop_event.set()
        executor.shutdown(wait=True)
        print("Shutdown complete.")
