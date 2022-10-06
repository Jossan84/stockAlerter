FROM python:3.8-slim-buster

WORKDIR /stockalert-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./data ./data
COPY ./app ./app

CMD [ "python", "./app/main.py" ]
