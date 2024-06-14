Purpose: This is a sample app that will show you the functionality of leveraging LaunchDarkly for components such as 
        enabling or disabling feature flags.

I.  Installation Prerequisites:

    A - While I personally recommend, PyCharm, as it will have Python, pip, and setup your venv. Otherwise, be sure to:
        1. Install Python, and pip
        2. create a virtual environment:
            python -m venv venv
            source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    B - Rather PyCharm or any IDE, install flask
          pip install Flask
    C - install dependencies (available under the requirments.txt) file
          pip install -r requirements.txt

II. App Setup:

    A - If you don't have one already, sign up for a LaunchDarkly account at launchdarkly.com (free trial available)
        1. Create a new project and copy your SDK key.
        2. within the app.py file, replace "YOUR SDK KEY" with your actual key.

III. App Utilization:

    A - within the command line enter:
         flask run
    B - you will see a link you can click, or open your browser and go to: http://127.0.0.1:5000 
        where you will be able to run the app on your local machine

IV. Flag Implementation:

    A - Create the following feature flags with the following names:
        'image-hint'
        'show-med-level'
    B - As you test turning on and off these features, you will notice that the app will turn off the "Hint button" 
        on the trivia question page, and also remove the Intermediate level option within the main page. 
        (The Image Hint feature response in real time without requiring a page refresh).

V. Optional - Integrations:

    I have created a Trello integration and Slack Integration. Trello's board can assist you with remediating feature flags. 
    For more information, please go to: https://docs.launchdarkly.com/integrations
