# Build Vue.js frontend
FROM node:14.5.0-alpine as build-stage

ARG VUE_APP_VERSION
ENV VUE_APP_VERSION=${VUE_APP_VERSION}

WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install --verbose
COPY ./frontend/ ./
RUN npm run build --verbose

# Setup Container and install Flask backend
FROM lsiobase/alpine:3.12 as deploy-stage
# MAINTAINER Your Name "info@selfhosted.pro"

# Set environment variables
ENV PYTHONIOENCODING=UTF-8
ENV THEME=Default

WORKDIR /api
COPY ./backend/requirements.txt ./

# Install build dependencies
RUN apk add --no-cache --virtual=build-dependencies \
    g++ \
    make \
    python3-dev \
    ruby-dev

# Install necessary system libraries for PyYAML and other Python packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    mysql-dev \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    nginx \
    python3-dev \
    g++ \
    make \
    jpeg-dev \
    zlib-dev \
    yaml-dev  # Adding this for PyYAML

# Upgrade pip, setuptools, and wheel
RUN pip3 install --upgrade pip setuptools wheel

# Install PyYAML with binary wheels only
RUN pip3 install PyYAML --only-binary :all:

# Install all Python modules from requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir --verbose

# Install SASS via gem
RUN gem install sass --verbose

# Clean up build dependencies
RUN apk del --purge build-dependencies && \
    rm -rf /root/.cache /tmp/*

# Copy the backend code
COPY ./backend/ ./

# Add any additional necessary setup commands here

# Expose ports and define the command to run the application
EXPOSE 5000
CMD ["python3", "app.py"]

