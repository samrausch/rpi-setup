from multiprocessing import Process
import socket
import time
import subprocess
import math
import os
import datetime
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Raspberry Pi pin configuration:
RST = None               # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()

displayMode = 0

def updateDisplay():

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        cmd = "service apache2 status | grep Active | cut -b 14-19"
        apache_status = subprocess.check_output(cmd, shell = True )
        cmd = "iwgetid | grep 'ESSID' | awk -F: '{print $2}' | sed      's/\"//g'"
        wifi_status = subprocess.check_output(cmd, shell = True )
        cmd = "date +%H:%M-%Z"
        date_time = subprocess.check_output(cmd, shell = True )

        if displayMode == 0:

                draw.text((x, top),"IP: " + str(IP.decode('utf8')),     font=font, fill=255)
                draw.text((x, top+8),"Apache: " + str(apache_status.decode('utf8')),    font=font, fill=255)
                draw.text((x, top+16),"Wifi: " + str(wifi_status.decode('utf8')),       font=font, fill=255)
                draw.text((x, top+25), "Prev             Ent             Next", font=font, fill=255)
                displayMode = 1

        else:

                draw.text((x, top),"            Time: " + str(date_time.decode('utf8')),        font=font, fill=255)
                draw.text((x, top+8),"Apache: " + str(apache_status.decode('utf8')),    font=font, fill=255)
                draw.text((x, top+16),"Wifi: " + str(wifi_status.decode('utf8')),       font=font, fill=255)
                draw.text((x, top+25), "Prev             Ent             Next", font=font, fill=255)
                displayMode = 0

        disp.image(image)
        disp.display()

def checkButtons():
        input1 = GPIO.input(26)
        if input1 == False:
                print("Button One")
        input2 = GPIO.input(19)
        if input2 == False:
                print("Button Two")
        input3 = GPIO.input(21)
        if input3 == False:
                print("Button Three")


while True:
        draw.text((x, top), "Hello world", font=font, fill=255)
        disp.image(image)
        disp.display()
        checkButtons
        updateDisplay
