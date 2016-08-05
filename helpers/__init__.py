from utils import coordinates, twilight, upload_files_s3, remove_files_os
from config import resolution, address, formats
from datetime import datetime, date
from fractions import Fraction

def _check_twilight(illumination=None):
	"""Check for daylight."""
	if illumination:
		illumination = illumination if date.today() == illumination[2] else twilight(coordinates(address))
	else:
		illumination = twilight(coordinates(address))
	result = 'daytime' if illumination[0] <= datetime.now() <= illumination[1] else 'nighttime'
	return (result, illumination)
	
def _daytime_attributes(camera):
	"""Set camera attributes for daytime."""
	camera.resolution = resolution
	camera.framerate = 30
	camera.shutter_speed = 0
	camera.iso = 0
	camera.exposure_mode = 'auto'
	return camera
	
def _nighttime_attributes(camera):
	"""Set camera attributes for nighttime. You may 
	   need to adjust these attributes for your
	   specific application."""
	camera.resolution = resolution
	camera.framerate = 30
	camera.shutter_speed = 0
	camera.iso = 800
	camera.exposure_mode = 'auto'
	return camera
	
def _set_attributes(status,camera):
	"""Set camera attributes based on twilight status."""
	camera = _daytime_attributes(camera) if status=='daytime' else _nighttime_attributes(camera)
	return (status,camera)

def _get_file_names(file_name):
	"""Get video and image file names."""
	file_names = ['.'.join([file_name,x]) for x in formats]
	return file_names

def _upload_and_remove_files(file_names):
	"""Upload video and image files to s3, 
	   then remove them from the system."""
	   files 
	try:
		upload_files_s3(file_names)
	except Exception:
		pass
	try:
		remove_files_os(file_names)
	except Exception:
		pass
