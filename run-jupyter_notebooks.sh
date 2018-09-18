#!/bin/bash

docker exec -it spark-master bash -c "cd /notebooks && jupyter notebook --ip=0.0.0.0 --no-browser --allow-root"