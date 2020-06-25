FROM lsiobase/alpine:3.12
#MAINTANER Your Name "info@selfhosted.pro"

ENV ADMIN_EMAIL=admin@yacht.local
ENV ADMIN_PASSWORD=password
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
	unzip \
    docker
WORKDIR /app
RUN  pip3 install -r requirements.txt
COPY app /app
COPY root /
COPY manage.py /
COPY config.py /
VOLUME /config
EXPOSE 5000



