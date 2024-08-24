

VERSION=v5
docker build . -t tarasenkoas/ton-exporter:$VERSION
docker push tarasenkoas/ton-exporter:$VERSION

#
# how to run ton-exporter locally
#

# (1) port-forward your liteserver

kubectl -n chains port-forward svc/ton 30003:30003


# (2) build & start

docker build . -t x \
  && docker run -it --rm \
    -e LITE_HOST=127.0.0.1 \
    -e LITE_PORT=30003 \
    -e LITE_PUB="xxxx=" \
    -e LITE_LABEL="local" \
    --network host x

# (3) query metrics

curl -s 0:8000/metrics


# (x) how to get liteserver public key:

python -c 'import codecs; f=open("liteserver.pub", "rb+"); pub=f.read()[4:]; print(str(codecs.encode(pub,"base64")).replace("\n",""))'

