FROM python3:8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN apk add build-essential libpoppler-cpp-dev pkg-config python3-dev

COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]