FROM ubuntu:20.04

WORKDIR /app

ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \ 
    build-essential \
    libpoppler58=0.41.0-0ubuntu1 \
    libpoppler-dev \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]