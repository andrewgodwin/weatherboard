import os
from io import BytesIO

from flask import Flask, send_file, request

from composer_2 import ImageComposer2
from composer_7 import ImageComposer7

app = Flask(__name__)


@app.route("/")
def index():
    config = {
        "latitutde": "39.75",
        "longitude": "-104.90",
        "timezone": "America/Denver",
        "country": "us",
        "font": "Roboto",
    }
    if os.environ.get("CONFIG"):
        import json
        config = json.load(open(os.environ.get("CONFIG")))
    config.update(request.args)

    # Get API key
    api_key = config.get("api_key")
    if not api_key:
        return '{"error": "no_api_key"}'
    # Render
    if config.get("style", "2") == "7":
        composer = ImageComposer7(**config)
        output = composer.render()
    else:
        composer = ImageComposer2(
            api_key,
            lat=config["latitude"],
            long=config["longitude"],
            timezone=config["timezone"],
        )
        image = composer.render()
        output = BytesIO()
        image.save(output, "PNG")
    # Send to client
    output.seek(0)
    return send_file(output, mimetype="image/png")
