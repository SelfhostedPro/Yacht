FROM lsiobase/alpine:3.12
#MAINTANER Your Name "info@selfhosted.pro"

ENV ADMIN_EMAIL=admin@yacht.local
ENV ADMIN_PASSWORD=password1
ENV FLASK_CONFIG=production
ENV PYTHONIOENCODING=UTF-8

COPY ./requirements.txt /app/requirements.txt
RUN \
 echo "**** install build packages ****" && \
 apk add --no-cache --virtual=build-dependencies \
	g++ \
	gcc \
	libxml2-dev \
	libxslt-dev \
	py3-pip \
	python3-dev \
    postgresql-dev &&\
 echo "**** install packages ****" && \
 apk add --no-cache \
    wget \
	python3 \
	unrar \
	unzip
WORKDIR /app
RUN  pip3 install -r requirements.txt
COPY /app /app
COPY /root /
COPY /storage /storage
VOLUME /storage
EXPOSE 5000

#####
# RUN apt-get update -y \
#  && apt-get install -y \
#     python3-pip python3-dev build-essential libpq-dev \
#  && rm -rf /var/lib/apt/lists/*

# # We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN pip3 install -r requirements.txt
# RUN pip3 install sqlalchemy_utils flask_dance flask_caching python-gitlab
# COPY . /app
# RUN python3 manage.py recreate_db && python3 manage.py setup_dev


