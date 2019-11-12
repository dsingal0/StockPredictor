from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS

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

