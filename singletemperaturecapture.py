import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
from phant import Phant
import configparser

config = configparser.ConfigParser()
		
config.read('../config/config.txt')
lat = config['location']['lat']
lon = config['location']['long']

publickey = config["sparkfun"]["publickey"]
privatekey = config["sparkfun"]["privatekey"]

p = Phant(public_key=publickey, fields=['humidity','lat','long','temp'],private_key=privatekey)



DHTpin = 23


RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

print(RHW)
print(TW)

p.log(2,2,2,2)
print(p.remaining_bytes, p.cap)
print("Test")

p.log(str(RHW),str(lat),str(lon),str(TW))
print(p.remaining_bytes, p.cap)

data = p.get()
print(data['temp'])

TWF = 9/5*TW+32

print(RHW)

print(TWF)
