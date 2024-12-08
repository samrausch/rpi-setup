#!/usr/bin/python3 -u

from multiprocessing import Process
import socket
import time
import datetime
import pytz
import RPi.GPIO as GPIO
import subprocess
import os
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

os.environ['TZ'] = "America/New_York"
time.tzset()

run = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

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

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 4

# Load default font.
font12 = ImageFont.truetype("/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMono.ttf", 12)
font14 = ImageFont.truetype("/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMono.ttf", 14)
font16 = ImageFont.truetype("/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMono.ttf", 16)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
        return(ip)
    except:
        ip = '127.0.0.1'
        return("No Address")
    finally:
        s.close()
        ip_split = ip.split(".")
while True:
       while run == 1: # Idle mode, nothing happening
           draw.rectangle((0, 0, width, height), outline=0, fill=0)
           draw.text((x, top),"IP: "+get_ip(), font=font12, fill=255)
           draw.text((x, bottom-14),time.strftime("%H:%M:%S", time.localtime()), font=font12, fill=255)
           disp.image(image)
           disp.display()

           input1 = GPIO.input(4)
           if input1 == False: # Go to PID mode
               draw.rectangle((0, 0, width, height), outline=0, fill=0)
               draw.text((x, top),"Server On Rebooting", font=font12, fill=255)
               disp.image(image)
               disp.display()
               time.sleep(5)
                bashCommand = "./wirelessServerEnable.sh"
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
               run = 2
           input2 = GPIO.input(17)
           if input2 == False: # Go to Idle mode
               draw.rectangle((0, 0, width, height), outline=0, fill=0)
               draw.text((x, top),"Server Off Rebooting", font=font12, fill=255)
               disp.image(image)
               disp.display()
               time.sleep(5)
        bashCommand = "./wirelessServerDisable.sh"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
               run = 1
           input3 = GPIO.input(22)
           if input3 == False:
               draw.rectangle((0, 0, width, height), outline=0, fill=0)
               draw.text((x, top),"Shutting Down!", font=font12, fill=255)
               disp.image(image)
               disp.display()
               bashCommand = "shutdown now"
               process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
               output, error = process.communicate()
               run = 5

           time.sleep(0.9)

       while run == 2: # PID mode, please be a PID
           draw.rectangle((0, 0, width, height), outline=0, fill=0)
           draw.text((x, top),"I'm a PID!", font=font16, fill=255)
           draw.text((x, bottom-18),time.strftime("%H:%M:%S", time.localtime()), font=font12, fill=255)
           disp.image(image)
           disp.display()

           input1 = GPIO.input(4)
           if input1 == False: # Go to PID mode
               draw.rectangle((0, 0, width, height), outline=0, fill=0)
               draw.text((x, top),"Going to PID!", font=font12, fill=255)
               disp.image(image)
               disp.display()
               time.sleep(5)
               run = 2
           input2 = GPIO.input(17)
           if input2 == False: # Go to Idle mode
               draw.rectangle((0, 0, width, height), outline=0, fill=0)
               draw.text((x, top),"Going to Idle!", font=font12, fill=255)
               disp.image(image)
               disp.display()
               time.sleep(5)
               run = 1
           input3 = GPIO.input(22)
           if input3 == False:
               draw.rectangle((0, 0, width, height), outline=0, fill=0)
               draw.text((x, top),"Shutting Down!", font=font12, fill=255)
               disp.image(image)
               disp.display()
               bashCommand = "shutdown now"
               process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
               output, error = process.communicate()
               run = 5

       while run == 5:
           exit()
