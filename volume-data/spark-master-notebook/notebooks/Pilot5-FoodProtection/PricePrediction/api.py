import string
import flask
import numpy as np
import json
import pickle
from flask import request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K



from os import path


app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
def home():
    return '''<h1>BigDataGrapes Product Price Prediction API</h1>
    <p> Available resources: <br>
    /api/v1/settings <br>
    /api/v1/productslist <br>
    /api/v1/priceprediction <br>
    </p>'''


@app.route('/api/v1/settings', methods=['GET'])
def settings():
    with open('settings.json') as json_file:
        settings_dic = json.load(json_file)
    
    constraints = settings_dic['constraints']
    configs = settings_dic['nn_configurations']
    constraints.update(configs)
    return jsonify(constraints)


@app.route('/api/v1/productslist', methods=['GET'])
def listofproducts():
    with open('settings.json', 'r', encoding='utf8') as json_file:
        settings_dic = json.load(json_file)
    
    mapping = settings_dic['product_name_id_mapping']
    return jsonify(mapping)


def load_prediction_model(product_id):
    model = load_model('models/product_id_{0}.h5'.format(product_id))
#     with open("models/product_id_{0}.pkl".format(product_id), "rb") as f:
#         model = pickle.load(f)
    model._make_predict_function()
    
    return model


@app.route('/api/v1/priceprediction', methods=['GET'])
def prediction():
    
    with open('settings.json', 'r', encoding='utf8') as json_file:
        settings_dic = json.load(json_file)

    if 'productid' in request.args :
        product_id = int(request.args['productid'])
    else:
        return "Error: No productid field provided. Please specify the productid param."

    if 'previousprice' in request.args:
        previous_price = str(request.args['previousprice']).replace('"','')
    else:
        return "Error: No previousprice field provided. Please specify the previousprice param."
    
    print("Query, ProductId:{0}, PreviousPrice:{1}".format(product_id, previous_price))
    
    steps = settings_dic['nn_configurations']['n_steps']
    if len(previous_price.split(","))!=steps:
        return "Error: invalid timeseries given for prediction."
    
    if not path.exists("models/product_id_{0}.h5".format(product_id)):
        return "Error: prediction model not found for the given product_id."
    
    # data preparation
    x = np.array([[float(n.translate(str.maketrans('', '', string.punctuation)))] for n in previous_price.split(",")])
    
    # load the scaler
    with open("scalers/product_id_{0}.pkl".format(product_id), "rb") as f:
        scaler = pickle.load(f)
    
    # normalize the data
    x = scaler.transform(x)
    x = x.reshape(1, x.shape[0], x.shape[1])
    
    #Before prediction
    K.clear_session()

    # load model
    model = load_prediction_model(product_id)        

    # predict and reverse value
    y = scaler.inverse_transform(model.predict(x))
    
    #After prediction
    K.clear_session()
    
    return jsonify({
        "productid": product_id,
        "predicted": str(y[0][0])
    })

app.run(host="0.0.0.0", port=8323)