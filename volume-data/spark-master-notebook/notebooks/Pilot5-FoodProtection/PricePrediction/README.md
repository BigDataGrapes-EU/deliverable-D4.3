
# H2020 RIA BigDataGrapes (T4.3) - Pilot 5 - Price Prediction 

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

## BigDataGrapes Predictive Data Analytics Demonstrators - Pilot 5 - Price Prediction

The specific goal of the price prediction is to develop a software module that allows to predict the future price of specific goods in the grapes and wines supply chain. Starting from past observations of the price of different agro/food items, we build a machine learning pipeline that allows us to experiment with several prediction solutions. 

#### Price Prediction Models

The python notebook **D4.3-PricePrediction-Pilot5.ipynb** should be used to train the prediction models. The trained models are saved at the folder /models. These models are then used by the REST API.

#### Price Prediction API

To start the API execute: 

```
$ python3 api.py
```

This command will start a local web service on port 8323
Make sure you have installed the necessary packages.   

Description of the available API resources: 
* **url:8323/api/v1/settings** - Returns the LSTM training setup.
* **url:8323/api/v1/productslist** - Returns a dictionary with the name of the products that the API is able to predict along with their corresponding ids. The Ids are used to query the priceprediction API resource.  
* **url:8323/api/v1/priceprediction** - Returns the next day product price prediction for a given product. 
Parameters:
productid: id of the product. (the produclist resource provides the products ids).  
previousprice: a previous price sequence. (the parameter "n_steps" at the settings resource indicates how many previous prices should be provided).   
Ex: url:8323/api/v1/priceprediction?productid=4&previousprice="220,234,265,240,230,236,227"
