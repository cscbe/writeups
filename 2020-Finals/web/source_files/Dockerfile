FROM python:3 AS tweeted
ENV PYTHONUNBUFFERED 1

# Adapted from https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py3/py3.6-xvfb-selenium/Dockerfile
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install xvfb
RUN apt-get install -yqq xvfb

# set display port to avoid crash
ENV DISPLAY=:99

RUN mkdir /code

# upgrade pip
RUN pip install --upgrade pip

WORKDIR /code
COPY ./application/requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./application/ /code/

COPY ./wait-for-it.sh /