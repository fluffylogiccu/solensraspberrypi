import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import configparser
import urllib.request

config = configparser.ConfigParser()
		
config.read('../config/config.txt')
lat = config['location']['lat']
lon = config['location']['long']
sensor_number = config['location']['sensornumber']
publickey = config["sparkfun"]["publickey"]
privatekey = config["sparkfun"]["privatekey"]


DHTpin = 23


humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

lat = str(lat)
lat = lat.replace('-','%2D')
lon = str(lon)
lon = lon.replace('-','%2D')
temp = str(temp)
temp = temp.replace('-','%2D')


request_string = "http://data.sparkfun.com/input/"+publickey+"?private_key="+privatekey
request_string = request_string + "&humidity="+str(humidity)+"&temp="+str(temp)
request_string = request_string + "&lat="+lat+"&long="+lon+"&sensornumber="+str(sensor_number)

print(request_string)
with urllib.request.urlopen(request_string) as f:
	data = f.read().decode('utf-8')	
print(data)
