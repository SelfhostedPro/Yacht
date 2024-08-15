# Setup Container and install Flask backend
FROM python:3.8-alpine as deploy-stage

# Set environment variables
ENV PYTHONIOENCODING=UTF-8
ENV THEME=Default

WORKDIR /api
COPY ./backend/requirements.txt ./

# Install build dependencies and system libraries
RUN apk add --no-cache \
    build-base \
    gcc \
    g++ \
    make \
    libffi-dev \
    openssl-dev \
    musl-dev \
    postgresql-dev \
    mysql-dev \
    jpeg-dev \
    zlib-dev \
    yaml-dev \
    python3-dev

# Upgrade pip, setuptools, and wheel
RUN pip3 install --upgrade pip setuptools wheel

# Install Cython explicitly to avoid issues with PyYAML
RUN pip3 install Cython --verbose

# Attempt to install PyYAML
RUN pip3 install --no-cache-dir --force-reinstall PyYAML==5.4.1 --verbose

# Install aiostream separately to troubleshoot installation issues
RUN pip3 install --use-pep517 aiostream==0.4.3 --no-cache-dir --verbose

# Install all remaining Python modules from requirements.txt
RUN pip3 install --use-pep517 -r requirements.txt --no-cache-dir --verbose

# Install SASS via gem
RUN apk add --no-cache ruby-dev && gem install sass --verbose

# Clean up build dependencies
RUN apk del --purge build-base && \
    rm -rf /root/.cache /tmp/*

# Copy the backend code
COPY ./backend/ ./

# Expose ports and define the command to run the application
EXPOSE 5000
CMD ["python3", "app.py"]