FROM python:alpine
RUN apk add --no-cache git
RUN mkdir /opt/yamix/; cd /opt/yamix/ && \
    git clone https://github.com/netinstall/yamix.git . && \
    pip3 install git+https://github.com/netinstall/yamix.git
CMD web.py
