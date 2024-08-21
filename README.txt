

VERSION=v3
docker build . -t tarasenkoas/ton-exporter:$VERSION
docker push tarasenkoas/ton-exporter:$VERSION



docker build . -t x \
  && docker run -it --rm \
    -e LITE_HOST=127.0.0.1 \
    -e LITE_PORT=30003 \
    -e LITE_PUB="xxxx=" \
    --network host x

curl -s 0:8000/metrics


# python -c 'import codecs; f=open("liteserver.pub", "rb+"); pub=f.read()[4:]; print(str(codecs.encode(pub,"base64")).replace("\n",""))'

