# H2020 RIA BigDataGrapes - Predictive Data Analytics (T4.3)

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets.

The BigDataGrapes platform aims at providing Predictive Data Analytics tools that go beyond the state-of-the-art for what regards their application to large and complex grapevine-related data assets. Having this ambitious goal in mind, the predictive analytics component described in this document has been designed by relying on the core technologies and frameworks for efficient processing of large datasets, e.g., Apache Spark, employed on the lower levels of the BDG platform. Machine learning largely benefits from the distributed execution paradigm that serves as the basis for addressing efficiently the analytics and scalability challenges of grapevines-powered industries. The software components enabling BDG predictive data analytics have been designed and deployed using Docker containers. They thus include everything needed to run the supported predictive data analytics tools on any system that can run a Docker engine.

The document first introduces the main technologies currently used in the first version of the BDG component for performing efficient and scalable analytics over extremely large dataset. The dockerized component provided in this deliverable relies on the BDG software stack discussed in Deliverable 2.3 "BigDataGrapes Software Stack Design" and exploits the distributed execution environment provided by the Persistence and Processing Layers of the BDG architecture contributed in Deliverable 4.1 "Methods and Tools for Scalable Distributed Processing".

The BDG platform allows the user to learn and apply predictive data analytics over extremely large dataset. We show these functionalities by discussing four demonstrators implemented as Jupyter Notebooks. The first three demonstrators deal with different kinds of machine learning tasks: regression, binary classification and multi-label classification. We present the three applications on three different datasets. The first one is synthetically generated while the other two are the KDD CUP 1999 dataset and the Red Wine Quality, both public. We first present how to train several kinds of models addressing the three tasks, i.e., linear regressors, random forest regressors, logistic regression classifiers by interacting with the BDG distributed infrastructure. We then present how to assess the performance of a learned model in terms of a well-known quality metric, i.e., Accuracy. Moreover, we present some basic visualization of the data to provide the user with a useful visual feedback.

The fourth demonstrator is much more complex and structured. It has been added to this document as an update done at M15. The demonstrator focuses on the application of machine learning methods on wine data collected from online social networks of wine passionate users. The dataset analysed contains: 489,417 wine reviews by 195,678 users, written in 86 languages, related to 306,856 different wines, from 57 wine countries and 2,120 wine regions. The predictive analysis conducted on this dataset allows us to show the potential of the machine learning layer of the BDG infrastructure providing efficient and effective methods for assessing the potential market penetration of a given wine on a new country. We estimate this penetration capability by learning a model from user-generated content about wines in the target country.

## BigDataGrapes Predictive Data Analytics Demonstrators

To get the code demonstrating the Predictive Data Analytics functionality of BDG, clone this GitHub repository

```
$ git clone https://github.com/BigDataGrapes-EU/deliverable-D4.3.git
```

The repository contains three Jupyter Notebooks and a Bash shell script that should be used to initialize the Big Data Grapes Platform. The script should be executed by running the Bash command below:

```
$ ./run-components.sh
```

The Bash script above downloads the Docker images and builds the environment according to the predefined configuration settings. The Bash script also starts the Docker containers of the BigDataGrapes software stack components.

Finally, to execute the demonstrators, run the following Bash command:  

```
$ ./run-jupyter_notebooks.sh
```

The Bash script above starts the Jupyter notebooks for predictive data analytics using the BigDataGrapes platform. To run the demonstrators, the user should point her browser to the following Jupyter Notebook URL: http://SERVER_URL:9999

The password used to protect the Jupyter Notebook instance is “bigdatagrapes”.

After a successful login the user can open the files below:
* D4.3-PredictiveDataAnalyticsWithMLLib-Regression-Py2.ipynb
* D4.3-PredictiveDataAnalyticsWithMLLib-Classification-Py2-KDDCUP1999.ipynb
* D4.3-PredictiveDataAnalyticsWithMLLib-MultiLabelClassification-Py2-WineDataset.ipynb
* D4.3-WineDataAnalysis-FlavorsTastes-PredictionUserRating.ipynb (for this Jupyter notebook we also made available an HTML version embedding all plots together.)

The execution of the code can be done by running each cell from the beginning to the end of each notebook and wait for the result.

## Useful BigDataGrapes Endpoints

* Apache HDFS Namenode: http://SERVER_URL:50070
* Apache HDFS Datanode: http://SERVER_URL:50075
* Spark-master: http://SERVER_URL:8080
* Spark-notebook: http://SERVER_URL:9001
* Hue (HDFS File Browser): http://SERVER_URL:8088/home
