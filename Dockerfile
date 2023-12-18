FROM python:3.10
WORKDIR /crawler
COPY requirements.txt requirements.txt
RUN apt update && apt install git -y && apt install libgomp1 libgbm-dev libasound2 -y
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt
# RUN playwright install && playwright install-deps
