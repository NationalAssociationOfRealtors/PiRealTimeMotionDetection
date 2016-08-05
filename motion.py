import numpy as np
from picamera import PiCamera, PiCameraCircularIO
from picamera.array import PiMotionAnalysis
from config import db, address, resolution, seconds,formats, sensitivity
from utils import coordinates, twilight, write_video,upload_files_s3,remove_files_os, save_motion
from helpers import _check_twilight, _daytime_attributes, _nighttime_attributes, _set_attributes,_get_file_names,_upload_and_remove_files
from datetime import datetime, date, time
from time import sleep

class DetectMotion(PiMotionAnalysis):
	"""Leverage PiMotionAnalysis class for real time
	   motion analysis. Return True if the magnitude
	   of motion is greater than the specified threshold."""
	def analyze(self, a):
		global result, magnitude
		a = np.sqrt(
				np.square(a['x'].astype(np.float)) +
				np.square(a['y'].astype(np.float))
				).clip(0, 255).astype(np.uint8)
		magnitude = (a > 60).sum() 
		threshold = sensitivity[0] if current_status=='daytime' else sensitivity[1]
		result = True if magnitude > threshold else False	
		return result

## Set initial values (while camera warms up)
result, magnitude = False, 0

with PiCamera() as camera:
	with DetectMotion(camera) as output:
		global current_status
		"""Set initial twilight settings and camera attributes.
		   Setup stream, start recording, then wait five seconds
		   for the camera to warm up (reduce false positives)."""
		prior_status, illumination = _check_twilight()
		#print prior_status, illumination
		camera = _set_attributes(prior_status,camera)[1]
		sleep(5)
		stream = PiCameraCircularIO(camera, seconds=seconds)
		camera.start_recording(stream, format=formats[0], motion_output=output) 
		try:
			while True:
				"""Update twilight status and check if current status 
				   is the same as prior status. If it is, then simply 
				   check for motion. If not, then daylight has changed
				   and we must update camera attributes."""
				current_status, illumination =_check_twilight(illumination)
				if current_status==prior_status:
					"""Implement camera.wait_recording(1) to wait on the 
					   video encoder for 1 timeout second. Modify timeout
					   seconds as necessary for your specific application.""" 
					if result:
						"""If result, motion detected. Capture start time, 
						   set file name, record magnnitude of motion, and
						   write the video."""
						#print "Motion Detected!"
						start = datetime.now()
						file_names, motion_magnitude = _get_file_names(start.isoformat()), magnitude
						camera.capture(file_names[1])
						write_video(stream,file_names[0])
						while result:
							"""While motion is detected, wait on the video
							   encoder for 6 timeout seconds. Modify timeout
							   seconds as necessary for your specific application.
							   The more timeout seconds, the more video captured 
							   after motion is detected."""
							camera.wait_recording(6)
						"""Motion ended. Capture end time, upload video to s3, 
						   remove video file from system, and save motion data
						   to db for analysis."""
						end = datetime.now()
						#print 'Motion Ended'
						_upload_and_remove_files(file_names)
						save_motion(start,end,motion_magnitude,file_names,current_status,illumination)	
				else:
					"""If daylight has changed, stop recording, swap 
					   camera attributes, and update twilight status. Then, 
					   start recording again. Wait five seconds for camera 
					   to warm up (reduce false positives)."""
					camera.stop_recording()
					prior_status, camera = _set_attributes(current_status,camera)
					sleep(5)
					camera.start_recording(stream, format=formats[0], motion_output=output)
		finally:
			camera.stop_recording()
