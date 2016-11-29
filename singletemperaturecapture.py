import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT



RCpin = 24
DHTpin = 23


GPIO.setmode(GPIO.BCM)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

TWF = 9/5*TW+32

print(RHW)

print(TWF)
