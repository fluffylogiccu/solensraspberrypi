from datetime import datetime, timedelta
import picamera
import sched, time
import dropbox
import configparser
import urllib.request
import json

class SolensImageCapture:
	def __init__(self):
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self.config = configparser.ConfigParser()
		self.camera = picamera.PiCamera()

		self.config.read('../config/config.txt')
		#Setup the dropbox credentials
		accesstoken = self.config['dropbox']['accesstoken']
		self.dbx = dropbox.Dropbox(accesstoken)
		lat = self.config['location']['lat']
		lon = self.config['location']['long']
		self.sunrise = self.get_sunrise(lat,lon)
		self.sunset = self.get_sunset(lat,lon)
		print(self.sunset)
		
		
	def get_sunrise(self,lat, lon):
		request_string = "http://api.sunrise-sunset.org/json?lat=" + lat + "&lng=" + lon + "&formatted=0"
		with urllib.request.urlopen(request_string) as f:
			data = json.loads(f.read().decode('utf-8'))
		sunrise = datetime.strptime(data['results']['sunrise'][:-6],'%Y-%m-%dT%H:%M:%S')
		return sunrise
		
	def get_sunset(self, lat, lon):
		request_string = "http://api.sunrise-sunset.org/json?lat=" + lat + "&lng=" + lon + "&formatted=0"
		with urllib.request.urlopen(request_string) as f:
			data = json.loads(f.read().decode('utf-8'))
		sunset = datetime.strptime(data['results']['sunset'][:-6],'%Y-%m-%dT%H:%M:%S')
		return sunset


if __name__ == "__main__":
	SolensImageCapture()
