from pymongo import MongoClient
from datetime import datetime, time
from boto3 import client

## MongoDB
db = MongoClient("")

## AWS s3
s3 = client("s3")
bucket = ""

## Camera resolution
resolution = (1280, 720)

## File formats (video, picture)
formats = ('h264','jpeg')

## PiCameraCircularIO number of seconds of video to
## store in memory until the write function is called. 
seconds = 12

## Motion sensitivity threshold (day, night). 
sensitivity = (10,6)

## Your address. If your exact address doesn't work, 
## or if you simply don't want to geocode your address, 
## use the next largest area like city, zip code, or state. 
## If all else fails, season defaults are set below. 
address = "Chicago, IL 60601"

## Default sunrise and sunset as datetime time object (e.g. time(h,m,s)). 
## If you specify your own values, we will not query 
## civil twilight.  
default_sunrise = None
default_sunset = None

## Default seasons.  
seasons = {1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',
		   6:'Summer',7:"Summer",8:"Summer",9:"Fall",10:"Fall",
		   11:"Fall",12:"Winter"}

## Default civil twilight values for various seasons.
## This is only used if your coordinates cannot be 
## identified by GoogleV3, and the correct twilights 
## by the sunrise-sunset api. If you don't know what 
## to use, you can keep these crude estimates (Chicago, IL).    
season_sunrise = {'Winter':time(5,46,0),'Spring':time(6,3,0), 
			'Summer':time(5,45,0), 'Fall': time(6,21,0)}
season_sunset = {'Winter':time(17,1,0),'Spring':time(18,30,0), 
		   'Summer':time(18,50,0),'Fall':time(17,45,0)}
