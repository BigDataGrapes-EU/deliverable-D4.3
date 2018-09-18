FROM bde2020/spark-worker:2.1.0-hadoop2.8-hive-java8

# install python essencials
RUN apt-get update && apt-get install -y python-setuptools python-dev build-essential

# install pip and jupyter
RUN easy_install pip && pip install jupyter

# install pyspark
RUN pip install pyspark
RUN pip install findspark
RUN pip install numpy
RUN pip install matplotlib

EXPOSE 8081