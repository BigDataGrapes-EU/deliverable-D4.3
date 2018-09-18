FROM bde2020/spark-master:2.1.0-hadoop2.8-hive-java8

# copy the xml setting for pydoop
COPY mapred-site.xml /etc/hadoop/

# MAINTAINER Vinicius Monteiro de Lira version: 0.1

# Install python essencials

RUN apt-get update && apt-get install -y python-setuptools python-dev build-essential

# install pip and jupyter
RUN easy_install pip && pip install jupyter && jupyter notebook --generate-config

# configure jupyter
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# install pyspark
RUN pip install pyspark
RUN pip install findspark
RUN pip install numpy
RUN pip install matplotlib
RUN pip install pydoop

# export PATH=/spark/bin/:$PATH
ENV PATH /spark/bin/:$PATH
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS 'notebook'
ENV PYTHONPATH $SPARK_HOME/python/:$PYTHONPATH


EXPOSE 8080
EXPOSE 7077
EXPOSE 9999