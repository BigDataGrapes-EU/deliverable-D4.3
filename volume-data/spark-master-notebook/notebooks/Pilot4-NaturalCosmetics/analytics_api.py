import flask
import json
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = False


# auxiliar method
def process_query(lab_property_type, top_k):

    dict_result = {
        "query": {
            "lab_prop_type": lab_property_type,
            "top_k": top_k
        }
    }
    
    # load file name
    filename = "analytics_api_{0}.json".format(lab_property_type)
    with open(filename) as json_file:
        correlation_data = json.load(json_file)
    
    # get top k
    for cor in correlation_data:
        cor['correlations'] = cor['correlations'][:top_k]
    
    dict_result.update({"results": correlation_data})
    
    return dict_result


@app.route('/', methods=['GET'])
def home():
    return '''<h1>BigDataGrapes Analytics API</h1><p></p>'''


@app.route('/api/v1/correlation/maceration', methods=['GET'])
def maceration():

    if 'topk' in request.args :
        top_k = int(request.args['topk'])
    else:
        top_k = 10
        # return "Error: No topk field provided. Please specify the labpropertytype param."

    lab_property_type = "Maceration"
    results = process_query(lab_property_type, top_k)
    
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/api/v1/correlation/ultrasound', methods=['GET'])
def ultrasound():

    if 'topk' in request.args :
        top_k = int(request.args['topk'])
    else:
        top_k = 10
        # return "Error: No topk field provided. Please specify the labpropertytype param."

    lab_property_type = "Ultrasound"
    results = process_query(lab_property_type, top_k)
    
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


app.run(host="0.0.0.0", port=8080)

