FROM base
LABEL manteiner="Andre Perez <andre.marcos.perez@gmail.com>"

# -- Layer: Image Metadata

ARG build_date

LABEL org.label-schema.build-date=${build_date}
LABEL org.label-schema.name="iFood MLOps App - Sandbox Image"
LABEL org.label-schema.url="https://github.com/andre-marcos-perez/ifood-mlops-app"
LABEL org.label-schema.schema-version="1.0"

# -- Layer: JupyterLab

ARG jupyterlab_version
RUN apt-get update -y && \
    pip3 install jupyterlab==${jupyterlab_version} && \
    rm -rf /var/lib/apt/lists/*

# -- Layer: Notebooks and data

ARG workspace=/opt/workspace
ADD sandbox/workspace/ ${workspace}/

# -- Runtime

EXPOSE 8888
VOLUME ${workspace}

WORKDIR ${workspace}
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=