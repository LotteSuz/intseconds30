FROM python:3.7-alpine

WORKDIR /code

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps \
    && apk add libc-dev

COPY . /code/

# Install packages
RUN pip install -r requirements.txt

# ENTRYPOINT ["/code/docker-entrypoint.sh"]