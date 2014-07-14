#!/usr/bin/env python

import argparse
import os
import signal
import sys
import time

import boto.route53

# example: route53.py \ 
# --name bob.example.com. \
# --type CNAME \
# --value alice.example.com \
# --zone example.com.
# NOTE: zone must end with full stop, and name must be FQDN, with full stop

parser = argparse.ArgumentParser(description='create dns record')
parser.add_argument('--name', metavar='<NAME>', default=os.environ.get('NAME'),
                    help='Name of DNS record')
parser.add_argument('--type', metavar='<TYPE>', default=os.environ.get('TYPE'),
                    help='Type of DNS record (A, CNAME, etc)')
parser.add_argument('--value', metavar='<VALUE>', default=os.environ.get('VALUE'),
                    help='Value of DNS record')
parser.add_argument('--zone', metavar='<ZONE>', default=os.environ.get('ZONE'),
                    help='Zone to add record to')
parser.add_argument('--ttl', metavar='<TTL>', default=300,
                    help='TTL of record')
args = parser.parse_args()

conn = boto.route53.Route53Connection()
zone = conn.get_zone(args.zone)

print "Creating record: {} {} {}".format(args.name, args.type, args.value)
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

zone.add_record(args.type, args.name, args.value, ttl=args.ttl)

print "Created."
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

def remove_record_func(zone, name, r_type, value):
    def handler(*args, **kwargs):
        print "Removing record: {} {} {}".format(name, r_type, value)

        rr = zone.find_records(name, r_type, 1)
        zone.delete_record(rr)

        print "Removed."
        sys.exit(0)
    return handler

remove = remove_record_func(zone, args.name, args.type, args.value)
signal.signal(signal.SIGTERM, remove)
signal.signal(signal.SIGINT, remove)

while True:
    time.sleep(5)
