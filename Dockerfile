# Docker image
FROM python:3.7-alpine3.8

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

# upgrade pip
RUN pip install --upgrade pip
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev

# Add maintainer
LABEL maintainer="Boris Nieto"
# Enviroment variable that prevents python-docker outputs problems
ENV PYTHONUNBUFFERED 1

# Add Postgresql client without cache, temp
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN apk del .tmp-build-deps

# Copy and run python dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# Create and set default scrap_tools folder
RUN mkdir /scrap_tools
WORKDIR /scrap_tools
COPY ./scrap_tools /scrap_tools
# Creating user and use it
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chown -R 755 /vol/web
USER user