import flask
import json
import pandas as pd
import numpy as np
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = False

# path to load


# auxiliar method
def fn_correlation_matrix(df_row, df_column, lst_properties_rows, lst_properties_columns, verbose=False):
    
    # build the correlation matrix
    correlation_matrix = np.ones((len(lst_properties_rows), len(lst_properties_columns)), dtype=np.float64)
    
    for i, prop_row in enumerate(lst_properties_rows):
        for j, prop_column in enumerate(lst_properties_columns):
            x_1 = np.array(df_row[prop_row].tolist())
            y_2 = np.array(df_column[prop_column].tolist())

            # np.corrcoef: returns pearson product-moment correlation coefficients.
            current_correlation = np.corrcoef(x_1, y_2)[0,1]
            correlation_matrix[i][j] = current_correlation
    
    return {
        "correlation_matrix": correlation_matrix.tolist(),
        "properties_rows": lst_properties_rows, 
        "properties_columns": lst_properties_columns
    }

@app.route('/', methods=['GET'])
def home():
    return '''<h1>BigDataGrapes Analytics API (Pilot 1)</h1><p></p>'''


@app.route('/api/v1/correlation/sensorvslab', methods=['GET'])
def sensorvslab():
    
    if 'topk' in request.args :
        top_k = int(request.args['topk'])
    else:
        top_k = 200

    # laod the dataset
    path_to_load = "../datasets/preprocessed_for_api/correlation_sensorvslab/"
    df_sensor = pd.read_csv(path_to_load + "df_sensor.csv")
    df_lab = pd.read_csv(path_to_load + "df_lab.csv")

    # features to correlate
    lst_sensor_properties = ['CV1m', 'Elevation']
    lst_lab_properties = ['pH', 'Titratable acidity (%)', '# of Grape Crates per cell', 'Sugar content (Brix%)', 'Mass of Harvested Product (Kg)']
    
    # adjust the vector size according to the availability of the data for the cells 
    cells_in_sensor_df = [c.replace("_", "") for c in df_sensor['cell'].unique()]
    df_lab = df_lab[df_lab['cell'].isin(cells_in_sensor_df)]

    # order by cell
    df_lab.sort_values(by="cell", inplace=True)
    df_sensor.sort_values(by="cell", inplace=True)
    
    df_sensor = df_sensor.head(top_k)
    df_lab = df_lab.head(top_k)

    # plot using data from 2019 only for the correlation analysis
    response = fn_correlation_matrix(df_lab, df_sensor, lst_lab_properties, lst_sensor_properties)
    
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(response)

@app.route('/api/v1/correlation/labvssatellite', methods=['GET'])
def labvssatellite():
    
    if 'topk' in request.args :
        top_k = int(request.args['topk'])
    else:
        top_k = 200

    path_to_load = "../datasets/preprocessed_for_api/correlation_labvssatellite/"
    df_lab = pd.read_csv(path_to_load + "df_lab.csv")
    df_satellite = pd.read_csv(path_to_load + "df_sat.csv")
    
    # properties
    lst_sat_properties = ['ndvi', 'ndre1', 'ndre2', 'ndwi', 'savi', 'evi2', 'cire']
    lst_lab_properties = ['pH', 'Titratable acidity (%)', '# of Grape Crates per cell', 'Sugar content (Brix%)', 'Mass of Harvested Product (Kg)']
    
    # 
    df_satellite = df_satellite.head(top_k)
    df_lab = df_lab.head(top_k)
    
    
    # correlation matrix
    response = fn_correlation_matrix(df_satellite, df_lab, lst_sat_properties, lst_lab_properties)
    
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(response)


@app.route('/api/v1/correlation/sensorvssatellite', methods=['GET'])
def sensorvssatellite():
    
    if 'topk' in request.args :
        top_k = int(request.args['topk'])
    else:
        top_k = 200

    path_to_load = "../datasets/preprocessed_for_api/correlation_sensorvssatellite/"
    df_sat = pd.read_csv(path_to_load + "df_sat.csv", nrows=top_k)
    df_sensor = pd.read_csv(path_to_load + "df_sensor.csv", nrows=top_k)
    
    # properties
    lst_sat_properties = ['ndvi', 'ndre1', 'ndre2', 'ndwi', 'savi', 'evi2', 'cire']
    lst_sensor_properties = ['RED', 'REDi', 'NIR', 'NIRi', 'NIRr', 'NDVI', 'LAI']
    
    # 
    df_sat = df_sat.head(top_k)
    df_sensor = df_sensor.head(top_k)
    
    # correlation matrix
    response = fn_correlation_matrix(df_sat, df_sensor, lst_sat_properties, lst_sensor_properties)
    
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(response)

app.run(host="0.0.0.0", port=8123)

