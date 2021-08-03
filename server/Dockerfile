FROM python:3.9-alpine

# Copy and install requirements
RUN apk update && apk add \
    gcc \
    g++ \
    freetype-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    python3-dev \
    cairo-dev

# Codebase setup
RUN mkdir /srv/weatherboard/
WORKDIR /srv/weatherboard/
RUN pip3 install requests pillow flask gunicorn pytz pycairo

# Add code
ENV PYTHONPATH /srv/weatherboard/server/
ADD . /srv/weatherboard/

# Add fonts
RUN mkdir /usr/share/fonts && cp /srv/weatherboard/fonts/Roboto* /usr/share/fonts && fc-cache

# Runtime
ENV PORT 80
CMD ["/bin/sh", "-c", "exec gunicorn --bind :$PORT --workers 1 --threads 8 server:app"]
