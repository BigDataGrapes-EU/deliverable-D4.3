import pandas as pd
import pickle

from flask import Flask, jsonify, request

# load the model
with open("./RandomForest.pkl", 'rb') as fp:
    model = pickle.load(fp)

app = Flask(__name__)
app.config["DEBUG"] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def api_root():
    return '''<h1>Water Balance Prediction API</h1>
    <p> Available resources: <br>
    /api/v1.0/predict_water_balance/single_observatio <br>
    /api/v1.0/predict_water_balance/full_dataset <br>
    </p>'''


@app.route('/api/v1.0/predict_water_balance/single_observation', methods=['GET'])
def predict_dataset_observation():
    dataset_id = request.args.get('dataset_id', default=1, type=int)
    observation_id = request.args.get('observation_id', default=1, type=int)

    print("You are requesting the water balance prediction of a observation in given dataset")

    if dataset_id == 1:
        dataset_file = "./data/casatoprimedonne2019_features_pulito.csv"
    elif dataset_id == 2:
        dataset_file = "./data/ilpalazzo2019_features_pulito.csv"
    else:
        return jsonify({'error': "Dataset not recognized!"})

    df_feature = pd.read_csv(dataset_file, header=None, sep=';', decimal=',')
    df_feature = df_feature.drop(columns=0)
    df_feature = df_feature.apply(pd.to_numeric, errors='coerce')

    X = df_feature.values

    if X.shape[0] < observation_id:
        return jsonify({'error': "Observation ID not present in the Dataset!"})

    pred = model.predict(X[observation_id:observation_id+1])

    return jsonify({'water_balance_prediction': pred[0]})


@app.route('/api/v1.0/predict_water_balance/full_dataset', methods=['GET'])
def predict_full_dataset():
    # if key doesn't exist, returns None
    dataset_id = request.args.get('dataset_id', default=1, type=int)

    print("You are requesting the water balance prediction of a observation in given dataset")

    if dataset_id == 1:
        dataset_file = "./data/casatoprimedonne2019_features_pulito.csv"
    elif dataset_id == 2:
        dataset_file = "./data/ilpalazzo2019_features_pulito.csv"
    else:
        return jsonify({'error': "Dataset not recognized!"})

    df_feature = pd.read_csv(dataset_file, header=None, sep=';', decimal=',')
    df_feature = df_feature.drop(columns=0)
    df_feature = df_feature.apply(pd.to_numeric, errors='coerce')

    X = df_feature.values

    preds = model.predict(X)

    return jsonify({'water_balance_prediction': preds.ravel().tolist()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8325)
