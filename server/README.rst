Weatherboard Server
===================

To setup::

    pip3 install requests pillow flask gunicorn pytz pycairo
    cp fonts/* /usr/share/fonts/
    fc-cache

To develop::

    FLASK_APP=server:app flask run --reload
