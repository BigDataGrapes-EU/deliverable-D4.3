FROM python:3.7-buster
COPY ./requirements.txt ./requirements.txt
COPY ./* ./
RUN python -m pip install pybind11
RUN python -m pip install -r ./requirements.txt
CMD ["python","api.py"]
