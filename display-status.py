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
    
    last_seconds = None
    while True:
        try:
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
            years, days, hours, minutes, seconds, microseconds = get_time_elapsed_elements()
            now_str = "%02dy %02dd %02d:%02d:%02d.%03d" % (years, days, hours, minutes, seconds, microseconds)
            sync_level_us = listener.sync_level
            sync_level_str = "0.0s"
            if sync_level_us > 0.0:
                sync_level_str = ("%.2fms" % (sync_level_us / 1000.0)) if sync_level_us > 1000 else ("%.2fus" % sync_level_us)
            sync_method_str = "no sync"
            if listener.sync_method:
                if listener.sync_method == "pps":
                    sync_method_str = "%d satellites" % listener.satellites_in_use
                elif listener.sync_method == "ntp":
                    sync_method_str = "ntp"
                
            sync_str = "±%s (%s)" % (sync_level_str, sync_method_str)
            is_new_second = (last_seconds is not None and seconds > last_seconds)
            last_seconds = seconds

            draw.text((0, 0), "Longplayer", font=font, fill=255)
            draw.text((0, 10), now_str, font=font, fill=255)
            draw.text((0, 20), sync_str, font=font, fill=255)

            if is_new_second:
                draw.rectangle((126, 0, 128, 1), outline=255, fill=255)

            disp.getbuffer(image)
            disp.ShowImage()
            time.sleep(.01)
        except(KeyboardInterrupt):
            print("\n")
            break

if __name__ == "__main__":
    main()

