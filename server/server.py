from io import BytesIO

from flask import Flask, send_file, request

from composer_2 import ImageComposer2
from composer_7 import ImageComposer7

app = Flask(__name__)


@app.route("/")
def index():
    # Get API key
    api_key = request.args.get("api_key")
    if not api_key:
        return '{"error": "no_api_key"}'
    # Render
    if request.args.get("style", "2") == "7":
        composer = ImageComposer7(
            api_key,
            lat=request.args.get("latitude", "39.75"),
            long=request.args.get("longitude", "-104.90"),
            timezone=request.args.get("timezone", "America/Denver"),
        )
        output = composer.render()
    else:
        composer = ImageComposer2(
            api_key,
            lat=request.args.get("latitude", "39.75"),
            long=request.args.get("longitude", "-104.90"),
            timezone=request.args.get("timezone", "America/Denver"),
        )
        image = composer.render()
        output = BytesIO()
        image.save(output, "PNG")
    # Send to client
    output.seek(0)
    return send_file(output, mimetype="image/png")
