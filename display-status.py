#!/usr/bin/env python3

import datetime
import time
import sys
import os
from oled_display import get_time_elapsed_elements
from oled_display import SyncStatsListener
from oled_display import SSD1305
from PIL import Image,ImageDraw,ImageFont

def main():
    listener = SyncStatsListener()
    
    # 128x32 display with hardware SPI:
    disp = SSD1305()
    
    # Initialize library.
    disp.Init()
    
    # Clear display.
    disp.clear()
    
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Load a TTF font
    # Some other fonts: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype('fonts/minecraftia-regular.ttf', 8)
    
    while True:
        try:
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
            years, days, hours, minutes, seconds, microseconds = get_time_elapsed_elements()
            now_str = "%02dy %02dd %02d:%02d:%02d.%03d" % (years, days, hours, minutes, seconds, microseconds)
            sync_str = "±%.2fus (%d satellites)" % (listener.pps_sync, listener.satellites_in_use)

            draw.text((0, 0), "Longplayer", font=font, fill=255)
            draw.text((0, 10), now_str, font=font, fill=255)
            draw.text((0, 20), sync_str, font=font, fill=255)

            disp.getbuffer(image)
            disp.ShowImage()
            time.sleep(.01)
        except(KeyboardInterrupt):
            print("\n")
            break

if __name__ == "__main__":
    main()

