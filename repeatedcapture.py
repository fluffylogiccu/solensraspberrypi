from datetime import datetime, timedelta
import picamera
import sched, time

s = sched.scheduler(time.time, time.sleep)

camera = picamera.PiCamera()


def camera_start():
	#calculate when to schedule the first image capture
	t = datetime.utcnow()
	t += timedelta(minutes = 1, seconds = -t.second, microseconds = -t.microsecond)
	print("First image will be captured at ", t)
	s.enterabs(time.mktime(t.timetuple()), 1, capture_image)
	#Start the scheduler
	s.run()



def capture_image():
	#take a picture
	camera.capture('/home/pi/FluffyLogic/Pictures/testimg1.jpg')
	#schedule the next image capture
	t = datetime.utcnow()
	if t.second == 30:
		t += timedelta(minutes = 1, seconds = -t.second, microseconds = -t.microsecond)
	else:
		t += timedelta(seconds = -t.second + 30, microseconds = -t.microsecond)
	print(t)
	s.enterabs(time.mktime(t.timetuple()), 1, capture_image)
	
if __name__ == "__main__":
	camera_start()
