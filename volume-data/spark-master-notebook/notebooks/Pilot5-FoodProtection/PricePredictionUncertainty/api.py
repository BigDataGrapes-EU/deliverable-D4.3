import subprocess
import string
import flask
import numpy as np
import json
import pickle

from flask import request, jsonify
from os import path

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['JSON_AS_ASCII'] = False

def load_data():
    data = []
    with open('Datasets/food_dataset_predictions.json') as f:
        for line in f:
            data.append(json.loads(line))
    return data  
    # 

@app.route('/', methods=['GET'])
def home():
    return '''<h1>BigDataGrapes Product Price Prediction API</h1>
    <p> Available resources: <br>
    /api/v1/food_data_predictions <br>
    /api/v1/products <br>
    /api/v1/product_predictions <br>
    /api/v1/countries_by_product <br>
    /api/v1/product_price_predictions <br>
    /api/v1/update_predictions <br>
    </p>'''

# test: /api/v1/products
@app.route('/api/v1/products', methods=['GET'])
def products():
    data = []
    with open('Datasets/products.json') as f:
        for line in f:
            data.append(json.loads(line))
        
    return jsonify(data)

# test: /api/v1/product_price_predictions?country=spain&product=virgin olive oil (up to 2°)
@app.route('/api/v1/product_price_predictions', methods=['GET'])
def product_price_predictions():
    product = request.args.get('product')
    country = request.args.get('country')
    
    if country is not None:
        return jsonify([x for x in data if x['product'] == product and x['country'] == country])
    else:
        return jsonify([x for x in data if x['product'] == product])

# test: /api/v1/countries_by_product?product=virgin olive oil (up to 2°)
@app.route('/api/v1/countries_by_product', methods=['GET'])
def countries_by_product():
    product = request.args.get('product')
    countries = list(set([x['country'] for x in data if x['product'] == product]))
    return jsonify(countries)

# test: /api/v1/products_by_country?country=greece
@app.route('/api/v1/products_by_country', methods=['GET'])                   
def products_by_country():
    country = request.args.get('country')
    products = list(set([x['product'] for x in data if x['country'] == country]))
    return jsonify(products)

@app.route('/api/v1/food_dataset_predictions', methods=['GET'])
def food_data_predictions():
    return jsonify(data)

@app.route('/api/v1/update_predictions', methods=['GET'])
def update_predictions():
    from subprocess import Popen
#     test = subprocess.Popen(["ping","-W","2","-c", "1", "192.168.1.70"], stdout=subprocess.PIPE)
#     output = test.communicate()[0]
#     print("output", output)
#     try:
#     process = subprocess.Popen(["Rscript","BDG_exploration.R"], stdout=subprocess.PIPE)
#     output = test.communicate()[0]
    
    print("Execute Rscript!")
    cmd = "Rscript BDG_exploration.R"
    execCmdLocal(cmd)
    print("Rscript executed!")

    return jsonify({"output": "The price predictions have been updated!"})


def execCmdLocal(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True )
    stdout, stderr = proc.communicate()
    status = proc.poll()
    if status != 0:
        print("Failed to execute command %s" % cmd)
    return status, stdout, stderr 


data = load_data()
app.run(host="0.0.0.0", port=8323)