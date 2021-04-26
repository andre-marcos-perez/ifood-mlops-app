FROM puckel/docker-airflow:1.10.9
LABEL manteiner="Andre Perez <andre.marcos.perez@gmail.com>"

# -- Layer: Image Metadata

ARG build_date

LABEL org.label-schema.build-date=${build_date}
LABEL org.label-schema.name="iFood MLOps App - Pipeline Image"
LABEL org.label-schema.url="https://github.com/andre-marcos-perez/ifood-mlops-app"
LABEL org.label-schema.schema-version="1.0"

# -- Layer: Requirements

USER root
COPY ./pipeline/requirements.txt requirements.txt

RUN apt-get update -y && \
    pip3 install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# -- Layer: Registry

ARG registry=/opt/registry
RUN mkdir -p ${registry}/
ENV REGISTRY=${registry}
