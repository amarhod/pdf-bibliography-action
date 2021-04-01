FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \ 
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]