FROM gettyimages/spark:2.3.1-hadoop-3.0
# MAINTAINER Vinicius Monteiro de Lira version: 0.1

# copy the xml setting for pydoop
COPY mapred-site.xml /etc/hadoop/

# conf spark
COPY spark-env.sh /usr/spark-2.3.1/conf/

# Install essential tools
RUN apt-get update && apt-get install -y python-setuptools python-dev build-essential ssh procps nano wget git zlib1g-dev libffi-dev

# install python 3.7
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz && tar xf Python-3.7.3.tar.xz && cd ./Python-3.7.3 && ./configure && make && make install
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.7 10

# install pip and jupyter
RUN pip3 install jupyter && jupyter notebook --generate-config

# configure jupyter
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# # install pyspark
RUN pip3 install pyspark findspark numpy matplotlib tensorflow pydoop scipy pandas tqdm seaborn sklearn keras plotly flask

# export PATH=/spark/bin/:$PATH
ENV PATH /spark/bin/:$PATH
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS 'notebook'
ENV PYTHONPATH $SPARK_HOME/python/:$PYTHONPATH


EXPOSE 8080
EXPOSE 7077
EXPOSE 9999