# Build Vue
FROM node:14.5.0-alpine as build-stage

ARG VUE_APP_VERSION
ENV VUE_APP_VERSION=${VUE_APP_VERSION}

WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ .
RUN npm run build

# Download docker for building images from compose files
# Not everything is needed so /usr/bin/docker can be copied
# out later to keep the overall image size small
RUN apk add docker-cli

# Setup Container and install Flask
FROM lsiobase/alpine:3.16 as deploy-stage
# MAINTANER Your Name "info@selfhosted.pro"

# Set Variables
ENV PYTHONIOENCODING=UTF-8
ENV THEME=Default

WORKDIR /api
COPY ./backend/requirements.txt .

# Install Dependancies
RUN \
	echo "**** install build packages ****" && \
	apk add --no-cache --virtual=build-dependencies \
	g++ \
	gcc \
	make \
	python3-dev \
	libffi-dev \
	libressl-dev \
	musl-dev \
	mysql-dev \
	postgresql-dev \
	openssl-dev \
	cargo \
	ruby-dev &&\
	echo "**** install packages ****" && \
	apk add --no-cache \
	python3 \
	py3-pip \
	nginx &&\
	pip3 install --upgrade pip &&\
	gem install sass &&\
	echo "**** Installing Python Modules ****" && \
	pip3 install wheel setuptools &&\
	printf '[global]\nextra-index-url=https://www.piwheels.org/simple' >/etc/pip.conf &&\
	CRYPTOGRAPHY_DONT_BUILD_RUST=1 pip3 install cryptography==3.4.8 &&\
	pip3 install -r requirements.txt &&\
	echo "**** Cleaning Up ****" &&\
	apk del --purge \
	build-dependencies && \
	rm -rf \
	/root/.cache \
	/tmp/*

COPY ./backend/api ./
COPY ./backend/alembic /alembic
COPY root ./backend/alembic.ini /

# Vue
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/

# Docker
COPY --from=build-stage /usr/bin/docker /usr/bin/docker

# Expose
VOLUME /config
EXPOSE 8000
