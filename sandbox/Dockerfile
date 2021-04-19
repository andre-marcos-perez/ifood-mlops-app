FROM base
LABEL manteiner="Andre Perez <andre.marcos.perez@gmail.com>"

# -- Layer: Image Metadata

ARG build_date

LABEL org.label-schema.build-date=${build_date}
LABEL org.label-schema.name="iFood MLOps App - Sandbox Image"
LABEL org.label-schema.url="https://github.com/andre-marcos-perez/ifood-mlops-app"
LABEL org.label-schema.schema-version="1.0"

# -- Layer: JupyterLab + Requirements

ARG jupyterlab_version
COPY ./sandbox/requirements.txt requirements.txt

RUN apt-get update -y && \
    pip3 install jupyterlab==${jupyterlab_version} && \
    pip3 install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# -- Layer: API

ARG customdir=/opt/python/custom
ADD ./api/ ${customdir}/api/

RUN echo "import sys\nsys.path.append('${customdir}')" > custom.py && \
    mkdir -p /root/.ipython/profile_default/startup/ && \
    mv custom.py /root/.ipython/profile_default/startup/custom.py

# -- Layer: Notebooks and data

ARG workspace=/opt/workspace
ADD ./sandbox/workspace/ ${workspace}/

# -- Runtime

EXPOSE 8888
VOLUME ${workspace}

WORKDIR ${workspace}
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=