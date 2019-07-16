from flask import request, jsonify, abort
import flask
import scrape_v2 as scrape
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import rake

app = flask.Flask(__name__)
app.config["DEBUG"] = True

options = Options()
chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# options.headless = True
# options=options, executable_path="/usr/local/Cellar/geckodriver/0.24.0/bin/geckodriver"
browser = webdriver.Chrome(options=options, chrome_options=chrome_options)


@app.route('/', methods=['GET'])
def home():
    string = "<h1>Quizlet Scraper API</h1><p>This site is a API for scraping quizlet sets for mc, and flashcards to port to your own service, download, or use</p>"
    instruct = "<br><p>your post request must include an 'id' and 'type'. The id is an integer representation of the quizlet quiz id, found in the URL for the quizlet. The type is either 'mc' (for a multiple choice json representation) or 'pure' (for a flashcard-like representation). </p>"
    return string + instruct


# @app.route('/api/v1/static/centers', methods=['GET'])
# def data():
#     return "hi"


'''
'type' parameter must be 'mc' or 'pure'
'id' parameter must be an int containing the id of the quizlet
'''
@app.route('/api/v1/get', methods=['POST'])
def find():
    if not request.json or not 'id' in request.json or not 'type' in request.json:
        abort(400)
    json = None
    if request.json['type'] == 'mc':
        json = scrape.getMultipleChoiceJson(request.json['id'], browser)
    else:
        json = scrape.getFlashcardsJson(request.json['id'], browser)
    task = {
        'id': request.json['id'],
        'data': json
    }
    return jsonify(task), 201


app.run()
