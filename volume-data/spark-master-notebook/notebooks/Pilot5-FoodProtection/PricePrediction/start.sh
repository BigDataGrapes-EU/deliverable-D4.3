#!/bin/bash

pwd

app="price_prediction"
docker build -t ${app} .
docker run -d -p 8323:8323 \
  --name=${app} \
  -v $PWD:/app ${app}
