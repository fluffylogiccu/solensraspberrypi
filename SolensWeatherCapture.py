import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT


class SolensWeatherCapture:
	def __init__(self):
		#DO TO MAKE THIS A CONFIG SETTING
		self.DHTpin = 23
		
		
	def get_temp_and_humidity:
		RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
		
		return (str(RHW), str(TW))
		
	
