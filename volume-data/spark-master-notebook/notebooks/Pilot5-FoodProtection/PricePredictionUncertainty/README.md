
# H2020 RIA BigDataGrapes (T4.3) - Pilot 5 - Price Prediction (with Time-Series Uncertainty version)

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

## BigDataGrapes Predictive Data Analytics Demonstrators - Pilot 5 - Price Prediction

The specific goal of the price prediction is to develop a software module that allows to predict the future price of specific goods in the grapes and wines supply chain. Starting from past observations of the price of different agro/food items, we build a machine learning pipeline that allows us to experiment with several prediction solutions. 

#### Price Prediction Models

The R file **BDG_exploration.R** should be used to train the prediction models and provide the predictions. These predictions are then used by the REST API.

#### Price Prediction API

To start the API execute: 

```
$ python3 api.py
```

This command will start a local web service on port 8323
Make sure you have installed the necessary packages.   


Available resources:
* **/api/v1/products** - Returns the list of all products. 
* **/api/v1/products_by_country** - Retrieve the list of products by country.
* **/api/v1/countries_by_product** - Retrieve the list of countries by product.
* **/api/v1/product_price_predictions** - Price predictions by country and product. The parameter country is optional.
* **/api/v1/update_predictions** - Update the prediction models. 

Ex: url:8323/api/v1/product_price_predictions?country=spain&product=virgin olive oil (up to 2°)
