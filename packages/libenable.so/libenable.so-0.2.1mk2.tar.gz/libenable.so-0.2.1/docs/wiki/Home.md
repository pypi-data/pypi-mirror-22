libenable.so Wiki
=================

libenable.so is a Python module designed to enable access to different protected
domains

Install
-------

To install libenable.so, you have a few options. libenable.so can either be used
as a docker container or from command line.

### Docker

libenable.so was designed and intended to run as a docker container and to be
accessed through it's RESTful web API. You can get it by first installing
[docker] and then pulling the image from the docker hub.

	docker pull bkvaluemeal/libenable.so

### Python

libenable.so can also be run from the command line. To do so, simply install it
with pip.

	pip install libenable.so

Usage
-----

Once libenable.so has been set up, you can run it like so:

### Docker

	docker run -d bkvaluemeal/libenable.so

### Python

	libenable --host localhost --port 80

Either way you run it, libenable.so will create a web interface where you can
browse and access the RESTful API. You can also browse the [documentation]
online.

[docker]: https://get.docker.com
[documentation]: https://bitbucket.org/bkvaluemeal/libenable.so/src/master/docs/api.md
