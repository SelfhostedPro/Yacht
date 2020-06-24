FROM python:3.8-slim

#MAINTANER Your Name "info@selfhosted.pro"

ENV ADMIN_EMAIL=admin@yacht.local
ENV ADMIN_PASSWORD=password
ENV SECRET_KEY=SuperRandomStringToBeUsedForEncryption
ENV FLASK_CONFIG=production
ENV PYTHONIOENCODING=UTF-8

RUN apt-get update -y \
 && apt-get install -y \
    python3-pip python3-dev build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install sqlalchemy_utils flask_dance flask_caching python-gitlab
COPY . /app
RUN python3 manage.py recreate_db && python3 manage.py setup_dev

CMD ["gunicorn", "--bind" ,"0.0.0.0:5000", "manage:app"]

