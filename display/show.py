#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import time

from waveshare_epd import epd5in83bc
from PIL import Image

IMAGE_SIZE = (600, 448)


def show_image(image):
    """
    Renders an image to the display. Handles splitting colours.
    """
    # Create red & black images of the right size
    black_image = Image.new("1", IMAGE_SIZE, 1)
    red_image = Image.new("1", IMAGE_SIZE, 1)
    # Copy pixels into them
    for x in range(IMAGE_SIZE[0]):
        for y in range(IMAGE_SIZE[1]):
            pixel = image.getpixel((x, y))
            if pixel[1] < 100:
                if pixel[0] > 125:
                    # Red
                    red_image.putpixel((x, y), 0)
                else:
                    # Black
                    black_image.putpixel((x, y), 0)
    # Send to the display
    epd = epd5in83bc.EPD()
    epd.init()
    epd.Clear()
    try:
        epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image))
        time.sleep(2)
    finally:
        epd.sleep()
