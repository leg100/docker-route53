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
# --zone example.com. \
# --weight 1 \
# --identifier bob-cname-to-alice
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
parser.add_argument('--weight', metavar='<WEIGHT>', default=os.environ.get('WEIGHT'),
                    help='Weighting of record')
parser.add_argument('--identifier', metavar='<IDENTIFIER>', default=os.environ.get('IDENTIFIER'),
                    help='Identifier to uniquely identify weighted record')
args = parser.parse_args()

conn = boto.route53.Route53Connection()
zone = conn.get_zone(args.zone)

rr = boto.route53.record.ResourceRecordSets(conn, zone.id)
r = rr.add_change('CREATE', args.name, args.type, ttl=args.ttl, weight=args.weight, identifier=args.identifier)

print "Creating record: {} {} {}".format(args.name, args.type, args.value)
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

r.add_value(args.value)
rr.commit()

print "Created."
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

def remove_record_func(zone, record):
    def handler(*args, **kwargs):

        print "Remove record: {} {} {}".format(record.name, record.type, record.resource_records[0])
        zone.delete_record(record)
        print "Removed."

        sys.exit(0)
    return handler

remove = remove_record_func(zone, r)
signal.signal(signal.SIGTERM, remove)
signal.signal(signal.SIGINT, remove)

while True:
    time.sleep(5)
