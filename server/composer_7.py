import datetime
import os
from io import BytesIO
from typing import Tuple

import pytz
import cairo

from weather import WeatherClient

# BLACK = 0
# WHITE = 1
# GREEN = 2
# BLUE = 3
# RED = 4
# YELLOW = 5
# ORANGE = 6
# PALETTE = [0,0,0,255,255,255,0,200,0,0,0,200,200,0,0,230,230,0,200,100,0]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
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
        self.weather = WeatherClient(self.lat, self.long)
        self.weather.load(self.api_key)
        # Create image
        with cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 448) as surface:
            context = cairo.Context(surface)
            context.rectangle(0, 0, 600, 448)
            context.set_source_rgb(1, 1, 1)
            context.fill()
            # Draw features
            self.draw_date(context)
            self.draw_temps(context)
            # Save out as bytestream
            output = BytesIO()
            surface.write_to_png(output)
            return output

    def draw_text(
        self,
        context: cairo.Context,
        text: str,
        position: Tuple[int, int],
        size: int,
        color=BLACK,
        weight="regular",
        align="left",
    ):
        text = str(text)
        if weight == "light":
            context.select_font_face("Roboto Light")
        elif weight == "bold":
            context.select_font_face(
                "Roboto", cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD
            )
        else:
            context.select_font_face("Roboto")
        context.set_source_rgb(*color)
        context.set_font_size(size)
        xbear, ybear, width, height = context.text_extents(text)[:4]
        if align == "center":
            context.move_to(position[0] - (width // 2) - xbear, position[1])
        else:
            context.move_to(*position)
        context.show_text(text)
        return width

    def draw_date(self, context: cairo.Context):
        now = datetime.datetime.now(self.timezone)
        # Day name
        left = 20
        left += self.draw_text(
            context,
            text=now.strftime("%A"),
            position=(20, 60),
            size=50,
            weight="light",
        )
        # Day number
        left += 10
        left += self.draw_text(
            context,
            text=now.strftime("%d").lstrip("0"),
            position=(left, 60),
            size=30,
            color=RED,
        )
        th = {
            "01": "st",
            "02": "nd",
            "03": "rd",
            "21": "st",
            "22": "nd",
            "23": "rd",
            "31": "st",
        }.get(now.strftime("%d"), "th")
        left += 6
        left += self.draw_text(
            context,
            text=th,
            position=(left, 50),
            size=20,
            color=RED,
        )
        # Month name (short)
        left += 7
        left += self.draw_text(
            context,
            text=now.strftime("%b"),
            position=(left, 60),
            size=30,
            color=RED,
        )

    def draw_temps(self, context: cairo.Context):
        # Draw on temperature ranges
        temp_min, temp_max = self.weather.temp_range_24hr()
        # Draw background rects
        context.rectangle(390, 10, 70, 65)
        context.set_source_rgb(*BLUE)
        context.fill()
        context.rectangle(530, 10, 70, 65)
        context.set_source_rgb(*RED)
        context.fill()
        self.draw_text(
            context,
            position=(425, 55),
            text=round(temp_min),
            color=WHITE,
            weight="bold",
            size=35,
            align="center",
        )
        self.draw_text(
            context,
            position=(495, 55),
            text=round(self.weather.temp_current()),
            color=BLACK,
            weight="bold",
            size=35,
            align="center",
        )
        self.draw_text(
            context,
            position=(565, 55),
            text=round(temp_max),
            color=WHITE,
            weight="bold",
            size=35,
            align="center",
        )

    def draw_meteogram(self, weather):
        last_temp_coords = None
        temp_min, temp_max = weather.temp_range_24hr()
        temp_range = temp_max - temp_min
        drawn_min = False
        drawn_max = False
        top = 120
        temp_height = 100
        precip_height = 100
        for hour in range(25):
            conditions = weather.hourly_summary(hour * 3600)
            x = 35 + (hour * 22)
            # Draw the hour every other hour
            if hour % 2 == 0:
                time_text = (
                    conditions["time"].astimezone(self.timezone).strftime("%H").lower()
                )
                self.draw_text(
                    pos=(x, top + 120),
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
                    (last_temp_coords[0], top + 110, x, top + 115),
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
            # Draw rain/snow bars
            precip_top = top + 165
            rain_height = min(precip_height, (conditions["rain"] / 8) * precip_height)
            snow_height = min(precip_height, (conditions["snow"] / 8) * precip_height)
            if rain_height:
                self.draw.rectangle(
                    (x - 3, precip_top, x + 3, precip_top + rain_height),
                    fill=BLUE,
                )
            if snow_height:
                self.draw.rectangle(
                    (
                        x - 3,
                        precip_top + rain_height,
                        x + 3,
                        precip_top + rain_height + snow_height,
                    ),
                    fill=GREEN,
                )
