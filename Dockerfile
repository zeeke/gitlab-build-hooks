FROM ubuntu:16.04

RUN \
  apt-get update -qq && \
  apt-get install -y \
    git \
    libcairo-dev \
    libedit-dev \
    python2.7 \
    python-pip

RUN pip install python-gitlab
RUN pip install py-trello

