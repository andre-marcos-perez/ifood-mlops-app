# Apps

<p align="center"><img src="image/mlops-docker.png"></p>

## 1. Sandbox

### 1.1. Description

The sandbox is built on JupyterLab interactive development environment is is meant to ease the interaction with the data
science team to develop and deploy ML model. It is shipped with api.ifood.mlop package, a Python SDK that glues the ML
platform together, essentially turning it into a "MLOps a Service" software model. With it user can create projects, run
experiments to train, test and deploy ML models.

### 1.2 Further Work

The Python SDK is missing a clear documentation (possibly with Sphinx) and lots of example notebooks to engage the data
science team with the ML platform. Also, the deployment process should be more auditable and restricted, possibly by a 
git pull request (or merge request) in between the experimental and deployment phases.
 
## 2. Database + Registry

### 2.1. Description

The database is built on MySQL and the Registry is built on a shared Docker volume, both are meant to register experiments
training, test and deployment data (database) and persist serialized models and their training and test data. They are
simple operational services that not only holds logical data that also tie together the ML platform apps but also adds a
layer os auditability and reproducibility to the whole ML model lifecycle.

### 2.2 Further Work

The registry could use a more robust object storage rather than a simple shared dir structure. Also the operational database
must be integrated with user info to audit experiment and deployment operations. 
 
## 3. Pipeline

### 3.1. Description

The pipeline is built on using Apache Airflow to orchestrate model training, testing and deployment. It is composed by two
types of dags: train-test dags and deployment dags. Train-test dags are meant to train and test models through experiments
that register hyper-params and performance metrics. The app reduces the data scientist freedom of defining their own test 
for the sake of performance since the responsible for delivering these high performance, possibly distributed (Dask, 
Apache Spark, etc.) is the ML engineering team. The deployment dag is meant to deploy the model for the serving layer. 
It updates the database and hits the serving API endpoint to load those models in memory to speed up the inference process.

### 3.2 Further Work

The train-test dags needs upgrades! More ML engine should be integrated (PyTorch, PyCaret, XGBoost, TensorFlow, etc.) 
through train-test dags. The deployment dags should give more freedom to the data science team to feature engine their 
own feature and possibly add business logic to the prediction, this can be achieved by turning the deliverable (pickle)
into a fully integrated microservice (a.k.a. docker) with its own endpoint.
 
## 4. Serving

### 4.1. Description

The serving API is built on the FastAPI project to server predictions. It contains two endpoints: predictions and 
models. The models endpoint dumps deployed models in memory to speed up inference process and the predictions endpoint 
generates the predictions and store them on the database. A x-api-key header simulates user authentication.

### 4.2 Further Work

Lots! A dedicated key-value caching database (a.k.a. Redis) should be used to cache predictions, a queued base system
could be used to avoid the prediction endpoint to directly access the database, models should be on their on 
microservice, making the serving API a interface between clients and models endpoints, scaling capacity with load balancers,
more effort must be put into the Swagger docs, etc.