from datetime import datetime, timedelta
from pytz import timezone
import pytz
import picamera
import sched, time
import dropbox
import configparser
import urllib.request
import json
import os
import logging

class SolensImageCapture:
	def __init__(self):
		logging.basicConfig(filename="SolensImageCapture.log",level=logging.INFO)
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self.config = configparser.ConfigParser()
		self.camera = picamera.PiCamera()

		self.config.read('../config/config.txt')
		#Setup the dropbox credentials
		accesstoken = self.config['dropbox']['accesstoken']
		self.dbx = dropbox.Dropbox(accesstoken)
		#Load location configuration
		self.lat = self.config['location']['lat']
		self.lon = self.config['location']['long']
		self.timezone = self.config['location']['timezone']
		logging.debug("LAT: " + self.lat)
		logging.debug("LONG: " + self.lon)
		logging.debug("TIMEZONE: " + self.timezone)
		self.sunrise = self.get_sunrise()
		self.sunset = self.get_sunset()
		self.s = sched.scheduler(time.time, time.sleep)
		
		
		
	def get_sunrise(self,tomorrow=False):
		day_in_Boulder = datetime.now(timezone(self.timezone))
		if tomorrow:
			day_in_Boulder += timedelta(days=1)
		request_string = "http://api.sunrise-sunset.org/json?lat=" + self.lat + "&lng=" + self.lon + "&formatted=0&date=" + day_in_Boulder.strftime("%Y-%m-%d")
		with urllib.request.urlopen(request_string) as f:
			data = json.loads(f.read().decode('utf-8'))
		sunrise = datetime.strptime(data['results']['sunrise'][:-6],'%Y-%m-%dT%H:%M:%S')
		logging.debug("Sunrise: ")
		logging.debug(sunrise.isoformat())
		return sunrise
		
	def get_sunset(self, tomorrow=False):
		day_in_Boulder = datetime.now(timezone(self.timezone))
		if tomorrow:
			day_in_Boulder += timedelta(days=1)
		request_string = "http://api.sunrise-sunset.org/json?lat=" + self.lat + "&lng=" + self.lon + "&formatted=0&date=" + day_in_Boulder.strftime("%Y-%m-%d")
		with urllib.request.urlopen(request_string) as f:
			data = json.loads(f.read().decode('utf-8'))
		sunset = datetime.strptime(data['results']['sunset'][:-6],'%Y-%m-%dT%H:%M:%S')
		logging.debug("Sunset: ")
		logging.debug(sunset.isoformat())
		return sunset
		
	def get_rounded_next_time(self):
		t = datetime.utcnow()
		if t.second >= 30:
			t += timedelta(minutes = 1, seconds = -t.second, microseconds = -t.microsecond)
		else:
			t += timedelta(seconds = -t.second + 30, microseconds = -t.microsecond)
		return t
		
	def day_time_loop(self, t):
			#take a picture
			imgname = t.isoformat() + "_" + self.lat + "_" + self.lon + ".jpg"
			self.camera.capture(imgname)
			#upload to dropbox
			with open(imgname,'rb') as f:
				data = f.read()
			imgname = '/' + imgname
			self.dbx.files_upload(data,imgname)
			#delete the image to save space
			os.remove(imgname[1:])

			#check for night time
			t = self.get_rounded_next_time()
			if t > self.sunset:
				#Night time, schedule next event for sunrise
				self.night_time()
			else:
				logging.debug("Next scheduled picture: " + t.isoformat())
				self.s.enterabs(time.mktime(t.timetuple()), 1, self.day_time_loop, argument = (t,))
				
	def night_time(self):
		logging.debug("Going to sleep")
		#update sunrise and sunset information for the next day
		self.sunrise = self.get_sunrise(tomorrow=True)
		self.sunset = self.get_sunset(tomorrow=True)
		logging.debug("Waking up tomorrow at " + self.sunrise.isoformat())
		self.s.enterabs(time.mktime(self.sunrise.timetuple()), 1, self.wake_up)
		
	def wake_up(self):
		logging.debug("Initialize image capture sequence...")
		t = self.get_rounded_next_time()
		logging.debug("Scheduling first image at " + t.isoformat())
		self.s.enterabs(time.mktime(t.timetuple()),1,self.day_time_loop, argument = (t,))


if __name__ == "__main__":
	#delay thirty seconds so when cron starts the script, the wifi has time to connect before uploading
	time.sleep(30)
	solens = SolensImageCapture()
	#check to see if the sun is up
	now_time = datetime.utcnow()
	#now_time += timedelta(hours = 6)
	if now_time > solens.sunrise and now_time < solens.sunset:
		logging.debug("The sun is up. Starting image capture")
		t = solens.get_rounded_next_time()
		solens.wake_up()
	else:
		logging.debug("The sun is down. Configuring wakeup for tomorrow at sunrise")
		solens.night_time()
	#start the scheduler
	solens.s.run()
