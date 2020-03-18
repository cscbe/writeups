FROM alpine:3.9

RUN apk add tcpdump ucspi-tcp

CMD tcpserver 0.0.0.0 80 tcpdump -w -
