# FROM python:3.10.0-alpine
FROM codingforentrepreneurs/python:3.9-webapp-cassandra

COPY ./app ./app/app
COPY ./requirements.txt ./app/requirements.txt

WORKDIR /app

# RUN python3 -m pip install -r requirements.txt
RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt

# CMD [ "executable" ]