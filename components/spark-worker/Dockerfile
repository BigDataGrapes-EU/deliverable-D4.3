FROM gettyimages/spark:2.3.1-hadoop-3.0

# install python essencials
RUN apt-get update && apt-get install -y python-setuptools python-dev build-essential
RUN apt-get install ssh procps nano wget git -y
# RUN apt-get update && apt-get install -y python-setuptools python-dev build-essential

# install jupyter
RUN pip install jupyter

# install pyspark
RUN pip install pyspark findspark numpy matplotlib

EXPOSE 8081

