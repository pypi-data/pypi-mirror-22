API
===

RESTful API

Documentation on how to use the RESTful API provided by the application

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Examples
--------

### Curl

	$ curl http://127.0.0.1:80/api/statistics
	$ curl http://127.0.0.1:80/api/recognize -F "image=<base64 encoded image>" -X POST
	$ curl http://127.0.0.1:80/api/tag -F "image=<base64 encoded image>" -X POST

### Python Requests

	import requests

	requests.get('http://127.0.0.1:80/api/statistics').json()
	requests.post('http://127.0.0.1:80/api/recognize', data = {'image': '<base64 encoded image>'}).json()
	requests.post('http://127.0.0.1:80/api/tag', data = {'image': '<base64 encoded image>'}).json()

The result of these examples is as follows:

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Version
-------

### GET

Returns the version of the application

	{
	  "version": "0.5.0"
	}

/api/version

Statistics
----------

### GET

Returns statistics about the application and the Python interpreter

	{
	  "python": {
	    "platform": "linux",
	    "version": "3.5.2"
	  },
	  "d3cryp7": {
	    "status_code": 1,
	    "version": "0.5.0",
	    "status": "WORKING",
	    "total_tasks": 29,
	    "running_tasks": 1
	  },
	  "time": {
	    "running": 39,
	    "start": 1482208973,
	    "current": 1482209012
	  }
	}

/api/statistics

Recognize
---------

### POST

Uses optical character recognition to extract text from an image

**Args:**

| Name  |      Description       |
|-------|------------------------|
| image | A base64 encoded image |

	{
	  "result": "The quick brown fox jumps over the lazy dog."
	}

/api/recognize

Tag
---

### POST

Uses machine learning to tag the contents of an image

**Args:**

| Name  |      Description       |
|-------|------------------------|
| image | A base64 encoded image |

	{
	  "result": {
	    "drive": 0.9986156,
	    "bumper": 0.97442794,
	    "coupe": 0.9619592,
	    "transportation system": 0.9958581,
	    "public show": 0.9867297,
	    "hood": 0.9648874,
	    "sedan": 0.97975063,
	    "fast": 0.9912327,
	    "engine": 0.9864018,
	    "wheel": 0.99912167,
	    "speed": 0.98680496,
	    "automotive": 0.9953874,
	    "horsepower": 0.9845407,
	    "roadster": 0.96291375,
	    "car": 0.99995154,
	    "headlight": 0.96830994,
	    "driver": 0.96466327,
	    "super": 0.9590338,
	    "vehicle": 0.9970878,
	    "hurry": 0.99164534
	  }
	}

/api/tag
