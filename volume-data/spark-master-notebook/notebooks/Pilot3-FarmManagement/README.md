
# H2020 RIA BigDataGrapes (T4.3) - Predictive Data Analytics (T4.3) 

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

## BigDataGrapes Predictive Data Analytics Demonstrators - Pilot 2 - Farm Management

The specific goal of the farm management pilot is to develop a machine-learning component that performs water balance prediction using meteorological data from weather stations and soil data.

#### Farm Management Model

The python notebook **D4.3-FarmManagement-Pilot3.ipynb** should be used to train the prediction model. The trained model is saved on file and then used by the REST API.

#### Farm Management API

To start the API execute: 

```
$ python3 api.py
```

This command will start a local web service on port 8325
Make sure you have installed the necessary packages.   

Description of the available API resources: 
* **url:8325/api/v1.0/predict_water_balance/single_observation** - Returns the water balance prediction of a single observation.   
* **url:8325/api/v1.0/predict_water_balance/full_dataset** - Returns water balance predictions for a all the observations contained in the given dataset. 
Parameters:
dataset_id: id of the dataset.  
observation_id: the id of the observation in the given dataset.   
"
