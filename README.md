# iFood MLOps App

> This repository is the documentation of my solution for the iFood ML Engineer test.

## 1. Getting Started

### 1.1. Introduction

### 1.2. Architecture

<p align="center"><img src="docs/image/mlops-docker.png"></p>

### 1.3. Applications

| App          | Address                                            | Description                                                 |
| ------------ | -------------------------------------------------- | ----------------------------------------------------------- |
| Sandbox      | [localhost:8888](http://localhost:8888/)           | Jupyter based env to develop, train, test and deploy models |
| Pipeline     | [localhost:8080](http://localhost:8080/)           | Apache Airflow based pipeline to train and test models      |
| Database     | [localhost:3306](http://localhost:3306/)           | MySQL based database to register ML experiments             |
| Serving API  | [localhost:8000](http://localhost:8000/)           | FastAPI based api to serve models prediction                |
| Serving Docs | [localhost:8000/docs](http://localhost:8000/docs/) | Swagger based web docs for serving api                      |

### 1.4. Pre-requisites

Install [Docker](https://docs.docker.com/get-docker/) (v1.13.0+) and [Docker Compose](https://docs.docker.com/compose/install/) (v1.10.0+).

## 2. Build

### 2.1. Local Build

> **Note**: Local build is currently only supported on Linux OS distributions.

```bash
./build.sh
```

### 2.2. Remote Build

Images are built

## 3. Run

If you build the images locally, you can start the platform by running the following command:

```bash
docker-compose -f up
```

If you'd like to use the images pre built and stored on Dockerhub, run the following command:

```bash
docker-compose -f docker-compose-remote.yml up
```
