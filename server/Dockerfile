FROM python:3.8-alpine

# Copy and install requirements
RUN apk update && apk add \
    gcc \
    g++ \
    freetype-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    python3-dev

# Codebase setup
RUN mkdir /srv/weatherboard/
WORKDIR /srv/weatherboard/
RUN pip3 install pillow flask gunicorn

# Add code
ENV PYTHONPATH /srv/weatherboard/server/
ADD . /srv/weatherboard/

# Runtime
ENV PORT 80
CMD ["/bin/sh", "-c", "exec gunicorn --bind :$PORT --workers 1 --threads 8 server:app"]
