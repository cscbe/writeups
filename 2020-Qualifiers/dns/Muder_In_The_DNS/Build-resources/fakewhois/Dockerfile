# docker build --tag dnsbelgium/fakewhois .
# docker run -d -p 43:4343 dnsbelgium/fakewhois

FROM centos:centos8

MAINTAINER <support@dnsbelgium.be>

COPY fakewhois /usr/local/bin/fakewhois

EXPOSE 4343/tcp

ENTRYPOINT /usr/local/bin/fakewhois
