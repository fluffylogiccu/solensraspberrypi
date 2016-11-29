import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT



DHTpin = 23


RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

TWF = 9/5*TW+32

print(RHW)

print(TWF)
