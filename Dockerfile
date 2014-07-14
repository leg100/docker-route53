FROM ubuntu:14.04
MAINTAINER Louis Garman "louisgarman@gmail.com"
#
# install deps/tools
#
RUN apt-get -q update 
RUN apt-get install -y python-boto

ADD route53.py route53.py

ENTRYPOINT ["/usr/bin/python", "route53.py"]
