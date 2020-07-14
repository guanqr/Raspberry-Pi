#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

#custom
from datetime import datetime
import requests
import RPi.GPIO

button1 = 5
button2 = 6
button3 = 13
button4 = 19

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(button1, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(button2, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(button3, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(button4, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

epd = epd2in7.EPD()
    
epd.init()
#epd.Clear(0xFF)
    
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font84 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 84)

#Location
Lct = ['hangzhou','beijing','tianjin','shanghai']
lct = Lct[0]
c = 0

def refreshWeather():
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    
    url = "https://api.seniverse.com/v3/weather/now.json?key=SVzUflQFz52yIkOVA&location="+lct+"&language=zh-Hans&unit=c"
    
    weaData = requests.get(url)
    cityName = weaData.json()['results'][0]['location']['name'] #city
    cityWea = weaData.json()['results'][0]['now']['text'] #weather
    cityTemp = weaData.json()['results'][0]['now']['temperature'] + '°C'#temp
    
    draw.text((10, 10), cityName, font = font36, fill = 0)
    draw.text((90, 10), cityWea, font = font36, fill = 0)
    draw.text((10, 50), cityTemp, font = font84, fill = 0)
    
    #show the refresh date
    dayTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    draw.text((10, 150), u'更新时间：', font = font16, fill = 0)
    draw.text((100, 150), dayTime, font = font16, fill = 0)
    
    epd.display(epd.getbuffer(Himage))

try:
    refreshWeather()
    while True:
        #time.sleep(1)
        if RPi.GPIO.input(button1) == 0:
            time.sleep(0.1)
            if RPi.GPIO.input(button1) == 0:
                c = c - 1
                if c < 0:
                    c = 3
                lct = Lct[c]
                refreshWeather()
        if RPi.GPIO.input(button2) == 0:
            time.sleep(0.1)
            if RPi.GPIO.input(button2) == 0:
                c = c + 1
                if c >= 4:
                    c = 0
                lct = Lct[c]
                refreshWeather()
        if RPi.GPIO.input(button3) == 0:
            epd.Clear(0xFF)
        if RPi.GPIO.input(button4) == 0:
            time.sleep(0.1)
            if RPi.GPIO.input(button4) == 0:
                epd2in7.epdconfig.module_exit()
                exit()
    
    #draw.line((20, 50, 70, 100), fill = 0)
    #draw.line((70, 50, 20, 100), fill = 0)
    #draw.rectangle((20, 50, 70, 100), outline = 0)
    #draw.line((165, 50, 165, 100), fill = 0)
    #draw.line((140, 75, 190, 75), fill = 0)
    #draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    #draw.rectangle((80, 50, 130, 100), fill = 0)
    #draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    #epd.display(epd.getbuffer(Himage))
    #time.sleep(2)

    #logging.info("Clear...")
    #epd.Clear(0xFF)
    
    #logging.info("Goto Sleep...")
    #epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
