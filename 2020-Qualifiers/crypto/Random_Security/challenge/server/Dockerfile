FROM alpine:3.9

RUN apk --update add python3 openssl ca-certificates tcpdump

RUN pip3 install flask

RUN mkdir /app
WORKDIR /app

ADD templates /app/templates
ADD run.py /app/run.py

EXPOSE 443

CMD python3 run.py