# Build Vue
FROM node:14.5.0-alpine as build-stage
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ .
RUN npm run build

# Setup Container and install Flask
FROM lsiobase/alpine:3.12 as deploy-stage
# MAINTANER Your Name "info@selfhosted.pro"

# Set Variables
ENV FLASK_CONFIG=production
ENV PYTHONIOENCODING=UTF-8

WORKDIR /api
COPY ./backend/requirements.txt .

# Install Dependancies
RUN \
 echo "**** install build packages ****" && \
 apk add --no-cache --virtual=build-dependencies \
	g++ \
	make \
	ruby-dev &&\
 echo "**** install packages ****" && \
 apk add --no-cache \
	python3 \
	py3-pip \
	nginx &&\
 gem install sass &&\
 echo "**** Installing Python Modules ****" && \
 pip3 install -r requirements.txt &&\
 echo "**** Cleaning Up ****" &&\
 apk del --purge \
	build-dependencies && \
 rm -rf \
	/root/.cache \
	/tmp/*

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