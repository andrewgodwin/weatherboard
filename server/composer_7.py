import datetime
import os

import pytz
from PIL import Image, ImageDraw, ImageFont

from weather import WeatherClient

IMAGE_SIZE = (600, 448)
WHITE = 0
BLACK = 1
RED = 2
GREEN = 3
BLUE = 4
YELLOW = 5
ORANGE = 6
PALETTE = [
    255,
    255,
    255,
    0,
    0,
    0,
    200,
    0,
    0,
    0,
    200,
    0,
    0,
    0,
    200,
    230,
    230,
    0,
    200,
    100,
    0,
]
fonts = {}
icons = {}


class ImageComposer7:
    def __init__(self, api_key, lat, long, timezone):
        self.api_key = api_key
        self.lat = lat
        self.long = long
        self.timezone = pytz.timezone(timezone)

    def render(self):
        # Fetch weather
        weather = WeatherClient(self.lat, self.long)
        weather.load(self.api_key)
        # Work out time
        now = datetime.datetime.now(self.timezone)
        # Create image
        self.image = Image.new("P", IMAGE_SIZE, 0)
        self.image.putpalette(PALETTE)
        # Draw on date
        self.draw = ImageDraw.ImageDraw(self.image)
        left = 15
        top = 7
        left += (
            self.draw_text(
                pos=(left, top),
                text=now.strftime("%A"),
                colour=BLACK,
                font=("light", 55),
            )[0]
            + 15
        )
        top += 23
        day_size = self.draw_text(
            pos=(left, top),
            text=now.strftime("%d").lstrip("0"),
            colour=RED,
            font=("regular", 28),
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
        th_size = self.draw_text(
            pos=(left, top), text=th, colour=RED, font=("regular", 20)
        )
        left += th_size[0] + 6
        self.draw_text(
            pos=(left, top),
            text=now.strftime("%b"),
            colour=BLACK,
            font=("bold", 28),
        )
        # Draw on temperature ranges
        temp_min, temp_max = weather.temp_range_24hr()
        self.draw.rectangle((390, 0, 460, 75), fill=BLUE)
        self.draw.rectangle((460, 0, 530, 75), fill=BLACK)
        self.draw.rectangle((530, 0, 600, 75), fill=RED)
        self.draw_text(
            pos=(425, 25),
            text=round(temp_min),
            colour=WHITE,
            font=("bold", 35),
            align="centre",
        )
        self.draw_text(
            pos=(495, 25),
            text=round(weather.temp_current()),
            colour=WHITE,
            font=("bold", 35),
            align="centre",
        )
        self.draw_text(
            pos=(565, 25),
            text=round(temp_max),
            colour=WHITE,
            font=("bold", 35),
            align="centre",
        )
        # Draw the meteogram
        self.draw_meteogram(weather)
        # Done!
        return self.image

    def draw_meteogram(self, weather):
        last_temp_coords = None
        temp_min, temp_max = weather.temp_range_24hr()
        temp_range = temp_max - temp_min
        drawn_min = False
        drawn_max = False
        top = 120
        temp_height = 80
        for hour in range(25):
            conditions = weather.hourly_summary(hour * 3600)
            x = 35 + (hour * 22)
            # Draw the hour every other hour
            if hour % 2 == 0:
                time_text = (
                    conditions["time"].astimezone(self.timezone).strftime("%H").lower()
                )
                self.draw_text(
                    pos=(x, top + 95),
                    text=time_text,
                    colour=BLACK,
                    font=("regular", 20),
                    align="centre",
                )
            # Draw sunlight/UV bar
            if last_temp_coords and conditions["uv"]:
                color = YELLOW
                if conditions["uv"] >= 3:
                    color = ORANGE
                if conditions["uv"] >= 8:
                    color = RED
                self.draw.rectangle(
                    (last_temp_coords[0], top + 85, x, top + 90),
                    fill=color,
                )
            # Draw temperature bar
            temp_y = top + (temp_max - conditions["temperature"]) * (
                temp_height // temp_range
            )
            temp_color = RED if conditions["temperature"] > 0 else BLUE
            if last_temp_coords:
                self.draw.line(
                    [last_temp_coords, (x, temp_y)],
                    fill=temp_color,
                    width=3,
                )
            last_temp_coords = (x, temp_y)
            # Draw min/max label if appropriate
            if conditions["temperature"] == temp_min and not drawn_min:
                self.draw_text(
                    pos=(x, temp_y - 30),
                    text=round(temp_min),
                    colour=temp_color,
                    font=("regular", 20),
                    align="centre",
                )
                drawn_min = True
            if conditions["temperature"] == temp_max and not drawn_max:
                self.draw_text(
                    pos=(x, temp_y + 5),
                    text=round(temp_max),
                    colour=temp_color,
                    font=("regular", 20),
                    align="centre",
                )
                drawn_max = True

    def draw_text(self, pos, text, colour, font, align="left"):
        """
        Draws text and returns its size
        """
        # Get font
        if font not in fonts:
            fonts[font] = ImageFont.truetype(
                "Roboto-%s.ttf" % font[0].title(), size=font[1]
            )
        # Calculate size
        size = self.draw.textsize(str(text), font=fonts[font])
        # Draw
        x, y = pos
        if align == "right":
            x -= size[0]
        elif align.startswith("cent"):
            x -= size[0] / 2
        self.draw.text((x, y), str(text), fill=colour, font=fonts[font])
        return size

    def size_text(self, text, font):
        """
        Returns text size
        """
        # Get font
        if font not in fonts:
            fonts[font] = ImageFont.truetype(
                "Roboto-%s.ttf" % font[0].title(), size=font[1]
            )
        # Calculate size
        return self.draw.textsize(str(text), font=fonts[font])

    def draw_icon(self, icon, pos, size):
        """
        Draws an icon file onto the image.
        """
        # Load icon
        if icon not in icons:
            raw_icon = Image.open(
                os.path.join(os.path.dirname(__file__), "icons-2", icon + ".png")
            ).convert("RGBA")
            palette_icon = Image.new("P", raw_icon.size, 0)
            for x in range(raw_icon.size[0]):
                for y in range(raw_icon.size[1]):
                    color = raw_icon.getpixel((x, y))
                    new_color = BLACK
                    if color[3] < 125:
                        new_color = WHITE
                    elif color[0] > 125:
                        if color[1] < 125:
                            new_color = RED
                        else:
                            new_color = WHITE
                    palette_icon.putpixel((x, y), new_color)
            icons[icon] = palette_icon
        # Resize
        icon_image = icons[icon].resize(size)
        self.image.paste(icon_image, pos)
