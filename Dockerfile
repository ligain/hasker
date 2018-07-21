FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y build-essential \
	    python3 \
	    python3-dev \
	    python3-pip

COPY . /opt/hasker

RUN pip3 install -r /opt/hasker/requirements/production.txt
EXPOSE 8000

ENV SECRET_KEY="3v35w9flnp(&f%g_64s0kl@@d=4y4%5!6kze^12rh&0&-stw_d"
ENV DJANGO_SETTINGS_MODULE="config.settings.production"
ENV DB_NAME="hasker"
ENV DB_USER="postgres"
ENV DB_PASSWORD="postgres"
ENV DB_HOST="db"
ENV DB_PORT="5432"

ENTRYPOINT python3 manage.py collectstatic --noinput \
    && uwsgi --ini /opt/hasker/uwsgi.ini
