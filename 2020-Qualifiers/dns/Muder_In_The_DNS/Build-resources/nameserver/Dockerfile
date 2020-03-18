# docker build --tag dnsbelgium/ikilledblack .
# docker run -d -p 53:53/udp -p 53:53 dnsbelgium/ikilledblack .

FROM centos:centos8

MAINTAINER <support@dnsbelgium.be>

COPY build-scripts/prepare_container.sh /tmp/prepare_container.sh
COPY build-scripts/start_named.sh /tmp/start_named.sh
COPY config/named.conf /etc/named.conf

RUN /bin/bash -x /tmp/prepare_container.sh

COPY --chown=named:named config/i-killed-black.be.zone /var/named/dynamic/i-killed-black.be/i-killed-black.be.zone

EXPOSE 53/udp 53/tcp

RUN chmod +x /tmp/start_named.sh
ENTRYPOINT /tmp/start_named.sh

