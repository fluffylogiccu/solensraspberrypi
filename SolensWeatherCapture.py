import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import sched, time
import logging
from datetime import datetime, timedelta
from phant import Phant
import configparser


class SolensWeatherCapture:
	def __init__(self):
		logging.basicConfig(filename="SolensWeatherCapture.log",level=logging.DEBUG)
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self.config = configparser.ConfigParser()
		
		self.config.read('../config/config.txt')
		self.DHTpin = self.config["weather"]["DHTpin"]
		#Load location configuration
		self.lat = self.config['location']['lat']
		self.lon = self.config['location']['long']
		
		self.publickey = self.config["sparkfun"]["publickey"]
		self.privatekey = self.config["sparkfun"]["privatekey"]
		
		self.p = Phant(public_key=self.publickey, fields=['temp','humid','lat','long'],private_key=self.privatekey)
		
		logging.debug("LAT: " + self.lat)
		logging.debug("LONG: " + self.lon)
		
		
	def loop(self):
		humidity, temp = self.get_temp_and_humidity()
		lat = self.lat
		lon = self.lon
		self.p.log(humidity, lat, lon, temp)
		
		t = self.get_rounded_next_time()
		
		self.scheduler.enterabs(time.mktime(t.timetuple()),1,self.loop)
		
	def get_temp_and_humidity(self):
		RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.DHTpin)
		
		return (RHW, TW)
		
	def get_rounded_next_time(self):
		t = datetime.utcnow()
		
		#t += timedelta(minutes = -(t.minute%5) + 5, seconds = -t.second, microseconds = -t.microsecond)
		t += timedelta(seconds = -t.second + 5, microseconds = -t.microsecond)
		
	

		return t
		
if __name__ == "__main__":
	solens = SolensWeatherCapture()
	
	logging.debug("Initialize weather capture sequence...")
	t = solens.get_rounded_next_time()
	logging.debug("Scheduling first weather capture at " + t.isoformat())
	solens.scheduler.enterabs(time.mktime(t.timetuple()),1,solens.loop)
	
	solens.scheduler.run()
		
	
