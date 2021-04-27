FROM debian:buster-slim
LABEL manteiner="Andre Perez <andre.marcos.perez@gmail.com>"

# -- Layer: OS + Python

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    pip3 install --upgrade pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# -- Runtime

CMD ["bash"]