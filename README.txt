

  docker build . -t tarasenkoas/ton-exporter:v1
  docker run -it --rm -p8000:8000 tarasenkoas/ton-exporter:v1

  curl -s 0:8000/metrics

  docker push tarasenkoas/ton-exporter:v1