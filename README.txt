

VERSION=v2
docker build . -t tarasenkoas/ton-exporter:$VERSION
docker push tarasenkoas/ton-exporter:$VERSION


  d build . -t x && dr -p8000:8000 x

  curl -s 0:8000/metrics
