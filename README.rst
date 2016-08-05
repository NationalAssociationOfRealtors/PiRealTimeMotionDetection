Realtime Motion Detection with Raspberry Pi
===========================================
This is a primitive solution for realtime motion detection 
with a Raspberry Pi. It's one component of a greater project to
build a simple, inexpensive, and functional surveliance 
system for a home or business. 

Features
--------

PiRealTimeMotionDetection has a set of basic features, namely
realtime motion detection, automatic lowlight adaptation, AWS integration
and MongoDB integration:

Realtime Motion Detection
~~~~~~~~~~~~~~~~~~~~~~~~~

The main feature of PiRealTimeMotionDetection is the ability to 
detect motion as it occurs in realtime. We leverage `picamera`_ 
to examine the amount of motion represented in successive video frames, 
and then record video and capture images when we observe motion events. 

.. _picamera: http://picamera.readthedocs.io/en/release-1.10/index.html

Automatic Lowlight Adaptation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We geocode your specified location, and then determine `civil twilight`_ for 
that location from the `Sunrise-Sunset API`_. Civil twilight is the limit at 
which solar illumination is sufficient for terrestrial objects to be clearly 
distinguished. Based on civil twilight, we automatically adjust the camera for 
both daytime and nighttime conditions. You can bypass the Sunrise-Sunset API by 
hardcoding your own constants, or setting constants for particular seasons.  

.. _`Sunrise-Sunset API`: http://sunrise-sunset.org/api.
.. _`civil twilight`: https://en.wikipedia.org/wiki/Twilight

AWS Integration
~~~~~~~~~~~~~~~

Automatically upload video and image data associated with motion events to 
AWS s3. This eliminates the need to store content on the Pi or an attached 
external harddrive. File names for video and image files are simply the full 
datetime of the start of the motion event, making it easy to find video and 
image data for specific motion events at a later date.       

MongoDB Integration
~~~~~~~~~~~~~~~~~~~

Store metadata for motion events in MongoDB. We capture the start time, 
end time, duration, and magnitude of motion events, along with the daylight
status at the time of motion, civil twilight used for that day, and file names 
for the data stored in s3. This makes it easy to analyze motion events, 
and then find specific motion event data in s3 should you determine that
a motion event is worth exploring in more detail. 

Setup
-----

Hardware:
::

    Raspberry Pi 3 Model B 
    Pi NoIR Camera V2 (infrared version)
    
Operating System:

::

    Raspbian


`AWS CLI`_: 

::

    [default]
	aws_access_key_id = access key ID
	aws_secret_access_key = secret access key
	region = aws-region

.. _`AWS CLI`: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html


Limitations
-----------

Some of our limitions include:
 
 	* Daytime and nighttime sensitivity thresholds that may not work for your specific application (expirement and refine). 
	* We assume some resonable level of natural or artificial light in lowlight conditions (i.e. moon, nearby street lights). 
	* Do not detect or adapt to adverse weather conditions.
	* We assume that your system time and timezone is properly configured. 
	* We assume that you've already created and configured AWS s3.
	* We assume that your MongoDB is running on a remote machine.
	* AWS and MongoDB integration is primitive.   
	* Weak logging and error handling.  


License
-------

The MIT License (MIT)

Copyright (c) 2016 National Association of REALTORS® 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
