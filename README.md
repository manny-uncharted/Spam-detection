# A spam detection model with full deployment instructions

## Setup

## How it works

An api endpoint that classifies messages as spam or not spam.

## Technologies used

- Python
- FastAPI
- Docker
- AWS EC2
- AWS S3
- Cassandra

## Features

Notes:
Remember to prune your docker environment using

```bash
docker system prune -a --volumes
```

This removes unused containers and images and makes space available on your instance.

Run using

```bash
docker run --restart always -e PORT=8001 -p 80:8001 -d <docker-image-name>
```

## Folder structure

```
├── README.md          <- The top-level README for developers using this project.
├── app                <- Source code for use in this project.
│   ├── __init__.py    <- Makes app a Python module
│   ├── main.py        <- FastAPI app
│   ├── models.py      <- Pydantic models for API endpoints
│   ├── ml.py     <- Functions for making predictions
│   ├── db.py     <- Functions for interacting with the database
│   ├── config.py     <- Configuration file
│   ├── schema.py   <- Database schema file.
├── notebooks
|   ├── download datasets.ipynb     <- Notebook for downloading datasets
|   ├── spam_classier_with_keras.ipynb  <- Notebook for training the model
|   ├── Encryption.ipynb    <- Notebook for creating an encryption key used by the project
├── datasets    <- contains the datasets used by the project
├── Dockerfile  <- Dockerfile for building the docker image
├── requirements.txt  <- The requirements file for reproducing the analysis environment
├── pipelines   <- Pypyr pipeline codes to download the model files from s3 bucket and decrypt the encrypted files.
```

## Run it locally

- Create a python virtual environment
- Install the requirements.txt file

  `pip install -r requirements.txt`
- Decrypt the app/encrypted file using

  `python3 -m pypyr pipelines/decrypt`
- Run the application

  `uvicorn app.main:app`
