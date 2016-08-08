import io
from os import remove
from picamera import PiVideoFrameType
from geopy import GoogleV3
from datetime import datetime, date
from urllib2 import Request, urlopen
from json import loads
from config import db,s3,bucket,seasons,season_sunrise,season_sunset, default_sunrise, default_sunset

def coordinates(address):
	"""We leverage GoogleV3 to geocode your specified location. 
	   Your location is used to determine the correct civil 
	   twilight, which helps with camera configuration.""" 
	client = GoogleV3()
	response = client.geocode(address)
	return (response.latitude, response.longitude)
	
def utconvert(civil_twilight_begin,civil_twilight_end):
	"""Crude universal time conversion."""
	date_format = "%Y-%m-%dT%H:%M:%S+00:00"
	offset = datetime.now() - datetime.utcnow()
	sunrise = datetime.strptime(civil_twilight_begin,date_format) + offset
	sunset = datetime.strptime(civil_twilight_end,date_format) + offset 
	return (sunrise, sunset)

def twilight(coordinates,default_sunrise=default_sunrise,default_sunset=default_sunset):
	"""We leverage civil twilight from http://sunrise-sunset.org/api. 
	   Civil twilight is the limit at which solar illumination 
	   is sufficient for terrestrial objects to be clearly distinguished. 
	   See here for additional info: https://en.wikipedia.org/wiki/Twilight"""
	today = date.today()
	season = seasons[today.month]
	if default_sunrise and default_sunset:
		sunrise = datetime.combine(today, default_sunrise)
		sunset = datetime.combine(today, default_sunset)
	else:
		try:
			url = "http://api.sunrise-sunset.org/json?lat=%s&lng=%sdate=today&formatted=0" % (coordinates[0],coordinates[1])
			req = Request(url)
			page = urlopen(req)
			response = loads(page.read())['results']
			sunrise, sunset = utconvert(response['civil_twilight_begin'],response['civil_twilight_end'])
		except Exception:
			sunrise = datetime.combine(today, season_sunrise[season])
			sunset = datetime.combine(today, season_sunset[season])
	return (sunrise,sunset,today)

def write_video(stream,file_name):
	"""Write video stream to the machine."""
	with stream.lock:
		for frame in stream.frames:
			if frame.frame_type == PiVideoFrameType.sps_header:
				stream.seek(frame.position)       
				break 

		with io.open(file_name, 'wb') as video:
			video.write(stream.read())

def upload_files_s3(file_names):
	"""Upload files to s3."""
	for item in file_names:
		try:
			s3.upload_file(item,bucket,item)
		except Exception:
			pass
	
def remove_files_os(file_names):
	"""Remove files from os."""
	for item in file_names:
		try:
			remove(item)
		except Exception:
			pass

def save_motion(start,end,magnitude,file_names,current_status,illumination):
	"""Save key motion data in the database."""
	try:
		db.pisecure.motion.insert({'start':start,'end':end,'duration':str(end-start),
			       'magnitude':magnitude,'file_names':file_names,'status':current_status, 
			       'civil_twilight_begin':illumination[0],'civil_twilight_end':illumination[1]})
	except Exception:
		pass 
			       	       
