# H2020 RIA BigDataGrapes - Predictive Data Analytics (T4.3)

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

## BigDataGrapes Predictive Data Analytics Demonstrators - Pilot 4 - Natural Cosmetics

We investigate how the biological activity depends on the location of the vineyard, the agriculture practices followed, the extraction method used, and the variety of the grape. The collected data from the natural cosmetics pilot will provide the necessary information for the evaluation of the quality of each sample, linked with the special characteristics of the vineyard of origin. Particularly, we developed a solution that uses relevant properties of the biological efficacy and correlates them with vegetation indexes derived from earth observations obtained from satellite imagery systems. 


#### Price Prediction API

To start the API execute: 

```
$ python3 analytics_api.py
```

This command will start a local web service on port 8080

Description of the available API resources: 
* **url:8323/api/v1/correlation/ultrasound** - Correlations between BA for ultrasound features and satellite image indexes
* **url:8323/api/v1/correlation/maceration** - Correlations between biological activity (BA) for ultrasound features and satellite image indexes


The python notebook **D4.3-CorrelationAnalysis-NaturalCosmetics-Pilot4.ipynb** can be used to visualize the heatmap of the correlation coefficients. 
