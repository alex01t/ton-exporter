FROM python:3.10.12

RUN apt-get update -qq \
  && apt-get install -qq \
    curl net-tools procps vim \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir asyncio fastapi[standard] pytoniq==0.1.39

WORKDIR /app
COPY main.py ./

CMD exec fastapi run --host 0.0.0.0 --port 8000 --workers 1

EXPOSE 8000
