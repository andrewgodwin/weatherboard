import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file

IMAGE_SIZE = (600, 448)
BLACK = 0
RED = 1
app = Flask(__name__)
fonts = {}


@app.route("/")
def index():
    now = datetime.datetime.now()
    # Create image
    image = Image.new("P", IMAGE_SIZE, 2)
    image.putpalette([0, 0, 0, 200, 0, 0, 255, 255, 255] + (252 * [0, 0, 0]))
    # Draw on date
    draw = ImageDraw.ImageDraw(image)
    left = 20
    top = 10
    draw_text(draw, left, top, now.strftime("%A"), BLACK, "light", 60)
    top += 65
    day_size = draw_text(
        draw, left, top, now.strftime("%d").lstrip("0"), RED, "regular", 30
    )
    left += day_size[0] + 2
    th = {
        "01": "st",
        "02": "nd",
        "03": "rd",
        "21": "st",
        "22": "nd",
        "23": "rd",
        "31": "st",
    }.get(now.strftime("%d"), "th")
    th_size = draw_text(draw, left, top, th, RED, "regular", 20)
    left += th_size[0] + 6
    draw_text(draw, left, 75, now.strftime("%B"), BLACK, "bold", 30)
    # Draw on weather
    temp_current, temp_max, temp_min = 23, 31, -3
    draw_text(draw, 470, 20, "°C", BLACK, "regular", 28, align="left")
    draw_text(draw, 470, 10, temp_current, BLACK, "regular", 90, align="right")
    draw_text(draw, 550, 15, temp_max, RED, "regular", 40, align="centre")
    draw_text(draw, 550, 60, temp_min, BLACK, "regular", 40, align="centre")
    # Send to client
    output = BytesIO()
    image.save(output, "PNG")
    output.seek(0)
    return send_file(output, mimetype="image/png")


def draw_text(draw, x, y, text, colour, font_style, font_size, align="left"):
    """
    Draws text and returns its size
    """
    # Get font
    if (font_style, font_size) not in fonts:
        fonts[font_style, font_size] = ImageFont.truetype(
            "Roboto-%s.ttf" % font_style.title(), size=font_size
        )
    # Calculate size
    size = draw.textsize(str(text), font=fonts[font_style, font_size])
    # Draw
    if align == "right":
        x -= size[0]
    elif align.startswith("cent"):
        x -= size[0] / 2
    draw.text((x, y), str(text), fill=colour, font=fonts[font_style, font_size])
    return size
