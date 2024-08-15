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
    postgresql-dev \
    python3-dev \
    libffi-dev \
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
    nginx

# Install Python modules
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt --verbose

# Install SASS via gem
RUN gem install sass --verbose

# Install Python modules
RUN pip3 install wheel --verbose
RUN pip3 install -r requirements.txt --verbose

# Clean up build dependencies
RUN apk del --purge build-dependencies && \
    rm -rf /root/.cache /tmp/*

# Copy the backend code
COPY ./backend/ ./

# Add any additional necessary setup commands here

# Expose ports and define the command to run the application
EXPOSE 5000
CMD ["python3", "app.py"]

