import picamera
import dropbox
import urllib.request
import time

camera = picamera.PiCamera()

f = open('../config/config.txt', 'r')

accesstoken = f.readline()
accesstoken = accesstoken.strip()

#dbx = dropbox.Dropbox(accesstoken)
camera.start_preview()
time.sleep(10)
camera.capture('testimg.jpg')
camera.stop_preview()

with open('testimg.jpg','rb') as f:
	data = f.read()

#dbx.files_upload(data,'/testimg.jpg')


#accesskey = f.readline()
#secretkey = f.readline()

#strip out the newlines
#accesskey = accesskey.strip('\n')
#secretkey = secretkey.strip('\n')

#print(accesskey)
#print(secretkey)



#camera.capture('/home/pi/FluffyLogic/Pictures/testimg.jpg')
