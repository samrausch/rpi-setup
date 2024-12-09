#!/usr/bin/python3 -u

from multiprocessing import Process
import socket
import time, threading
import datetime
#import pytz
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

displayUpdateLast = 0
displayUpdateDelay = 0.9


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button 4
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 3
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 2
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 1

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
font12 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
font14 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
font16 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)


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

ipAddress = get_ip()

def displayUpdate():
    cmd = "service hostapd status | grep Active"
    hostapd_status = str(subprocess.check_output(cmd, shell = True ),'utf-8').split(":")[1].split(" ")[1]

    cmd = "service plexmediaserver status | grep Active"
    plex_status = str(subprocess.check_output(cmd, shell = True ),'utf-8').split(":")[1].split(" ")[1]

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top),"IP: "+ipAddress, font=font12, fill=255)
    draw.text((x, top+12),"APd: "+hostapd_status, font=font12, fill=255)
    draw.text((x, top+24),"Plex: "+plex_status, font=font12, fill=255)
    draw.text((x, top+48),time.strftime("%H:%M:%S", time.localtime()), font=font12, fill=255)
    disp.image(image)
    disp.display()

    input1 = GPIO.input(4)
    if input1 == False: # Start wireless server
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top),"Turning Server On", font=font12, fill=255)
        draw.text((x, top+12),"Rebooting...", font=font12, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(5)
        bashCommand = "./wirelessServerEnable.sh"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    input2 = GPIO.input(17)
    if input2 == False: # Stop wireless server
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top),"Turning Server Off", font=font12, fill=255)
        draw.text((x, top+12),"Rebooting...", font=font12, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(5)
        bashCommand = "./wirelessServerDisable.sh"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    input3 = GPIO.input(22)
    if input3 == False: # Shut down
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top),"Shutting Down!", font=font12, fill=255)
        disp.image(image)
        disp.display()
        bashCommand = "shutdown now"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        time.sleep(0.9)
    threading.Timer(0.9, displayUpdate).start()

#while True:
#    if time.time() > displayUpdateLast + displayUpdateDelay:
#        displayUpdate()
#        displayUpdateLast = time.time()
displayUpdate()
while True:
    time.sleep(0.01)
