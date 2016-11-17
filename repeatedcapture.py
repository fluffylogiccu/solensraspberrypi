from datetime import datetime, timedelta
import picamera
import sched, time
import dropbox
import configparser
import urllib.request
import json

s = sched.scheduler(time.time, time.sleep)
config = configparser.ConfigParser()
camera = picamera.PiCamera()

config.read('../config/config.txt')
#Setup the dropbox credentials
accesstoken = config['dropbox']['accesstoken']
dbx = dropbox.Dropbox(accesstoken)



def camera_start():
	#Determine sunrise sunset times
	lat = config['location']['lat']
	lon = config['location']['long']
	request_string = "http://api.sunrise-sunset.org/json?lat=" + lat + "&lng=" + lon + "&formatted=0"
	with urllib.request.urlopen(request_string) as f:
		data = json.loads(f.read().decode('utf-8'))
	print(data['results']['sunrise'])
	#calculate when to schedule the first image capture
	t = datetime.utcnow()
	t += timedelta(minutes = 1, seconds = -t.second, microseconds = -t.microsecond)
	print("First image will be captured at ", t)
	s.enterabs(time.mktime(t.timetuple()), 1, capture_image, argument = (t,))
	#Start the scheduler
	s.run()



def capture_image(t):
	#take a picture
	imgname = t.isoformat() + ".jpg"
	camera.capture(imgname)
	#upload to dropbox
	with open(imgname,'rb') as f:
		data = f.read()
	imgname = '/' + imgname
	dbx.files_upload(data,imgname)

	#schedule the next image capture
	if t.second == 30:
		t += timedelta(minutes = 1, seconds = -t.second, microseconds = -t.microsecond)
	else:
		t += timedelta(seconds = -t.second + 30, microseconds = -t.microsecond)
	print(t)
	s.enterabs(time.mktime(t.timetuple()), 1, capture_image, argument = (t,))
	
if __name__ == "__main__":
	camera_start()
