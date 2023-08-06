API
===

RESTful API

Documentation on how to use the RESTful API provided by the application

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Examples
--------

### Curl

	$ curl http://127.0.0.1:80/api/statistics

### Python Requests

	import requests

	requests.get('http://127.0.0.1:80/api/statistics').json()

The result of these examples is as follows:

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Version
-------

### GET

Returns the version of the application

	{
	  "version": "0.2.1"
	}

/api/version

Statistics
----------

### GET

Returns statistics about the application and the Python interpreter

	{
	  "libenable": {
	    "version": "0.2.1",
	    "status": "RUNNING",
	    "running_tasks": 0,
	    "total_tasks": 0,
	    "status_code": 0
	  },
		"python": {
	    "platform": "linux",
	    "version": "3.5.2"
	  },
	  "time": {
	    "running": 123,
	    "start": 1483303416,
	    "current": 1483303539
	  }
	}

/api/statistics

reCAPTCHA
---------

### POST

Enables access to reCAPTCHA protected domains

**Args:**

|   Name   |          Description           |
|----------|--------------------------------|
| site_key | The site key of the domain     |
| url      | String | The URL of the domain |

	{
	  "result": "03AHJ_VusHdHs4pPNqGC95gyF...I5WsvJLzjwD-j4wFrUAaxju7o"
	}

/api/reCAPTCHA

Solve Media
----------

### POST

Enables access to Solve Media protected domains

**Args:**

|   Name   |        Description         |
|----------|----------------------------|
| site_key | The site key of the domain |

	{
	  "result": {
	    "response": "agree to disagree",
	    "challenge": "2@mlFwzmfg.OLZWwwByqjR...HEedbHGOTFGZrJkhFXIK0uoA"
	  }
	}

/api/solvemedia
