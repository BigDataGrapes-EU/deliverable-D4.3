# H2020 RIA BigDataGrapes - Predictive Data Analytics (T4.3)

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

## BigDataGrapes Predictive Data Analytics Demonstrators - Pilot 1 - Table Wine Grapes

The goal of this pilot is to allow the user to explore and visualize the correlations in the sensor and phenological farming data collected in all test sites located in Greece to understand and explain what affects grape quality and yield.

#### Analytical API

To start the API execute: 

```
$ python3 analytics_api.py
```

This command will start a local web service on port 8123

Description of the available API resources: 
* **url:8323/api/v1/correlation/sensorvslab** - handles associations and correlations between precision agriculture information (sensor data) and phenological data and grape chemical analysis (lab data).
* **url:8323/api/v1/correlation/labvssatellite** - correlates lab data with earth observation data from satellite imagery.
* **url:8323/api/v1/correlation/sensorvssatellite** - correlates the sensor data with earth observation data on vegetation indexes (NDVI) for similar dates.

The python notebook **D4.3-CorrelationAnalysis-TableWineGrapes-Pilot1.ipynb** can be used to visualize the heatmap of the correlation coefficients. 
