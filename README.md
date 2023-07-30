# A spam detection model with full deployment instructions

## Setup


## How it works



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