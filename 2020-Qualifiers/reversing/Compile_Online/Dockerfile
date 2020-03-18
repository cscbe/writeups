FROM alpine:3.9

RUN apk add gcc ucspi-tcp musl-dev

CMD echo $CO_FLAG > flag.txt; \
    echo $CO_FLAG >> /etc/passwd; \
    tcpserver 0.0.0.0 80 sh -c \
     "timeout -t 5 cat - | gcc -o /dev/stdout -xc - 2>&1"
