from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/api/random', endpoint='randomFunc')
def random_number():
    response = {
        'randomNumber': randint(101, 200)
    }
    return jsonify(response)

@app.route('/api/goog', endpoint='googleFunc')
def random_number():
    response = {
        'googleValue': randint(1000, 2000)
    }
    return jsonify(response)

@app.route('/api/headers', endpoint='getStockHeaders')
def stock_headers():
    response = {
        'stockHeaders': getTickersSP500()
    }
    return jsonify(response)

def getTickersSP500():
  LIST_OF_COMPANIES_WIKI = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  website_url = requests.get(LIST_OF_COMPANIES_WIKI).text
  soup = BeautifulSoup(website_url, "html.parser")
  my_table = soup.find('table',{'class':'wikitable sortable', 'id': "constituents"})
  label_items = my_table.findAll('a', {'class': 'external text', 'rel': 'nofollow'})
  labels = []
  for label_item in label_items:
    label = label_item.get_text()
    if label == 'reports' or label == 'Aptiv Plc':
        continue
    labels.append(label)
  return labels