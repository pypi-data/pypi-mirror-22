d3cryp7.py Wiki
===============

d3cryp7.py is a Python module for image analysis and recognition designed to
decode, decrypt and understand the contents of an image.

Install
-------

To install d3cryp7.py, you have a few options. d3cryp7.py can either be used as
a docker container or from command line.

### Docker

d3cryp7.py was designed and intended to run as a docker container and to be
accessed through it's RESTful web API. You can get it by first installing
[docker] and then pulling the image from the docker hub.

	docker pull bkvaluemeal/d3cryp7.py

### Python

d3cryp7.py can also be run from the command line. To do so, simply install it
with pip.

	pip install d3cryp7.py

Usage
-----

Once d3cryp7.py has been set up, you can run it like so:

### Docker

	docker run -d bkvaluemeal/d3cryp7.py

### Python

	d3cryp7 --host localhost --port 80

Either way you run it, d3cryp7.py will create a web interface where you can
browse and access the RESTful API. You can also browse the [documentation]
online.

[docker]: https://get.docker.com
[documentation]: https://bitbucket.org/bkvaluemeal/d3cryp7.py/src/master/docs/api.md
