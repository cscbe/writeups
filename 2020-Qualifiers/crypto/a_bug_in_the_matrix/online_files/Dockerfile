FROM haskell:8

EXPOSE 5555/tcp

WORKDIR /usr/src/app
COPY Challenge.hs .
RUN cabal update
RUN cabal install random --lib
RUN ghc Challenge.hs

RUN apt update
RUN apt install socat -y
COPY socat_server.sh .

ENV FLAG=CSCBE{So_those_algebra_classes_did_have_a_use?}
ENTRYPOINT ./socat_server.sh
