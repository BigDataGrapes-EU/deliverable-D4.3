
# H2020 RIA BigDataGrapes (T4.3) - Predictive Data Analytics (T4.3) 

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

## BigDataGrapes Predictive Data Analytics Demonstrators - Pilot 2 - Wine Making

The specific goal of the wine making pilot is to develop a machine-learned pipeline aiming at counting leaves from side-view grapevine images taken into the imaging cabin of the PhenoArch platform (see picture below) managed by INRA.

#### Wine Making Model

The python notebook **D4.3-WineMaking-Pilot2.ipynb** should be used to train the prediction model. The trained model is saved at the current folder. This model is then used by the REST API.

#### Wine Making API

To start the API execute: 

```
$ python3 api.py
```

This command will start a local web service on port 8325
Make sure you have installed the necessary packages.   

Description of the available API resources: 
* **url:8325/api/v1.0/predict_dataset/** - Returns a list of the predicted number of leaves for each image in the given dataset.   
* **url:8325/api/v1.0/predict_image/** - Returns the predicted number of leaves for a single image in the given dataset. 
Parameters:
dataset_id: id of the dataset.  
image: an id to a given image.   
"