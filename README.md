# H2020 RIA BigDataGrapes - Predictive Data Analytics (T4.3)

The deliverable D4.3 (Models and Tools for Predictive Analytics over Extremely Large Datasets) describes the first version of the mechanisms and tools supporting efficient and effective predictive data analytics over the BigDataGrapes (BDG) platform in the context of grapevine-related assets. 

The BDG software stack employs efficient and fault-tolerant tools for distributed processing, aimed at providing scalability and reliability for the target applications. On top of this stack, the BDG platform enables distributed predictive big data analytics by effectively exploiting scalable Machine Learning algorithms using efficiently the computational resources of the underlying infrastructure. The software components enabling BDG predictive data analytics have been designed and deployed using Docker containers. They thus include everything needed to run the supported predictive data analytics tools on any system that can run a Docker engine. 

The document first introduces the main technologies currently used in the first version of the BDG component for performing efficient and scalable analytics over extremely large dataset. The docker component provided in this deliverable relies on the BDG software stack discussed in Deliverable 2.3 "BigDataGrapes Software Stack Design" and exploits the distributed execution environment provided by the Persistence and Processing Layers of the BDG architecture contributed in Deliverable 4.1 "Methods and Tools for Scalable Distributed Processing". The document details the steps to be followed to download and deploy the first version of the BDG platform and provides the reader with practical examples of usage of its scalable predictive analytics component. Specifically, we provide three demonstrators released as Jupyter Notebooks implementing three different machine learning tasks by exploiting the BDG infrastructure. The first one shows how to train two kinds of regressors, i.e., linear and random forest regressors, to fit synthetically generated data. We present these results by adding a visualization of the result to allow the reader to understand the limitations of each specific solution. The second demonstrator employs a well-known dataset, i.e., the KDD CUP 1999 dataset, to train a binary logistic regression classifier. We show how to train and evaluate the performance of the classifier by means of a standard metric, i.e., Accuracy. This second demonstrator also shows how the distributed filesystem can be exploited to directly feed with data the machine learning platform. The third demonstrator extends the second one by showing how to train a multi-label classifier on the Red Wine Quality Dataset, a public dataset employed on Kaggle for a machine learning competition. We show how to learn a multi label logistic regression classifier and how to evaluate its performance in terms of Accuracy.

In this first version of D4.3 we assess the effectiveness of different predictive data analytics tools in terms of a standard and popular metrics such as Accuracy. Future versions of the BDG predictive analytics component will provide tools and methods for a deep analysis of the performance of different machine learning libraries by specifically considering the results of WP7 (Cross-sector Rigorous Experimental Testing).

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

The Bash script above starts the Jupyter notebooks for predictive data analytics using the BigDataGrapes platform. To run the demonstrators, the user should point her browser to the following Jupyter Notebook URL: http://<server_address>:9999

The password used to protect the Jupyter Notebook instance is “bigdatagrapes”.

After a successful login the user can open the files below:
* D4.3-PredictiveDataAnalyticsWithMLLib-Regression-Py2.ipynb
* D4.3-PredictiveDataAnalyticsWithMLLib-Classification-Py2-KDDCUP1999.ipynb
* D4.3-PredictiveDataAnalyticsWithMLLib-MultiLabelClassification-Py2-WineDataset.ipynb

The execution of the code can be done by running each cell from the beginning to the end of each notebook and wait for the result.


## Useful BigDataGrapes Endpoints

* Apache HDFS Namenode: http://SERVER_URL:50070
* Apache HDFS Datanode: http://SERVER_URL:50075
* Spark-master: http://SERVER_URL:8080
* Spark-notebook: http://SERVER_URL:9001
* Hue (HDFS File Browser): http://SERVER_URL:8088/home
