FROM python:3.10.12

RUN pip3 install --no-cache-dir asyncio fastapi[standard] pytoniq==0.1.39

WORKDIR /app
ADD https://ton.org/global-config.json ./config.json
#COPY config.json ./
COPY main.py ./

CMD PYTHONUNBUFFERED=1 fastapi run --host 0.0.0.0 --port 8000 --workers 1

EXPOSE 8000
