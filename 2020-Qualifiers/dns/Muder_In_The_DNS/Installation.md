# Installation instructions

* copy containers.tar to the docker hosts with ips `52.31.129.243` and `54.154.165.103`
* on both hosts run `docker image load -i containers.tar`
* on the host with ip `54.154.165.103` run the command `docker run -d -p 43:4343 dnsbelgium/fakewhois`
* on the host with ip `52.31.129.243` run the command `docker run -d -p 53:53/udp -p 53:53 dnsbelgium/ikilledblack`
