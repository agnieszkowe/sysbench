FROM ubuntu

RUN apt-get update \
    && apt-get install -y sysbench bonnie++ \
    && mkdir /boonie-tests \
    && chmod 777 /boonie-tests \
    && useradd -m agnieszkowe \
    && rm -rf /var/lib/apt/lists/*
