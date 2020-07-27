FROM gettyimages/spark:2.3.1-hadoop-3.0
# MAINTAINER Vinicius Monteiro de Lira version: 0.1

# copy the xml setting for pydoop
COPY mapred-site.xml /etc/hadoop/

# conf spark
COPY spark-env.sh /usr/spark-2.3.1/conf/

# Install essential tools
RUN apt-get update && apt-get install -y python-setuptools python-dev build-essential ssh procps nano wget git

# install pip and jupyter
RUN easy_install pip && pip install jupyter && jupyter notebook --generate-config

# configure jupyter
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# install pyspark
RUN pip tensorflow
RUN pip install pyspark findspark numpy matplotlib pydoop scipy pandas pickle tqdm seaborn sklearn keras plotly flask

# export PATH=/spark/bin/:$PATH
ENV PATH /spark/bin/:$PATH
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS 'notebook'
ENV PYTHONPATH $SPARK_HOME/python/:$PYTHONPATH


EXPOSE 8080
EXPOSE 7077
EXPOSE 9999