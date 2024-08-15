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

# Install necessary system libraries for Python packages
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
    yaml-dev

# Upgrade pip, setuptools, and wheel
RUN pip3 install --upgrade pip setuptools wheel

# Install Cython explicitly to avoid issues with PyYAML
RUN pip3 install Cython

# Install PyYAML using binary wheel to avoid building from source
RUN pip3 install --only-binary :all: PyYAML

# Install aiostream separately to troubleshoot installation issues
RUN pip3 install --use-pep517 aiostream==0.4.3 --no-cache-dir --verbose

# Install all remaining Python modules from requirements.txt
RUN pip3 install --use-pep517 -r requirements.txt --no-cache-dir --verbose

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

