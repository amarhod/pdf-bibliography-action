FROM ubuntu:20.04

WORKDIR /app

ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \ 
    build-essential \
    libpoppler-dev \
    libpoppler-cpp-dev \
    poppler-utils \
    pkg-config \
    python3-dev

COPY . /app

RUN pip3 install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]