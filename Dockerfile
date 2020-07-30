# Build Vue
FROM node:14.5.0-alpine as build-stage
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ .
RUN npm run build

# Setup Container
FROM lsiobase/alpine:3.12 as deploy-stage
# MAINTANER Your Name "info@selfhosted.pro"

# Set Variables
ENV FLASK_CONFIG=production
ENV PYTHONIOENCODING=UTF-8

# Install Dependancies
RUN \
 echo "**** install build packages ****" && \
 apk add --no-cache --virtual=build-dependencies \
	g++ \
	gcc \
	libxml2-dev \
	libxslt-dev \
	py3-pip \
	make \
	ruby-dev \
	python3-dev &&\
 echo "**** install packages ****" && \
 apk add --no-cache \
	python3 \
    docker \
	nginx &&\
 gem install sass

# Flask
WORKDIR /api
COPY ./backend/requirements.txt .
RUN  pip3 install -r requirements.txt
RUN apk del --purge --no-cache \
	g++ \
	gcc \
	libxml2-dev \
	py3-pip \
	python3-dev \
	make \
	ruby-dev

COPY ./backend/api .
COPY root /
COPY ./backend/manage.py /
COPY ./backend/config.py /

# Vue
COPY --from=build-stage /app/dist /app
COPY nginx.conf /config/nginx/nginx.conf

# Expose
VOLUME /config
EXPOSE 8000