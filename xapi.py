#!/usr/bin/env python

import time, sys, os, os.path
import XenAPI
from subprocess import call

def find_service():
	for path in [ "/sbin/service", "/usr/sbin/service" ]:
		if os.path.exists(path):
			return path
	print >>sys.stderr, "I don't know how to start and stop services on this platform"
	exit(1)

def is_service_running(name):
	try:
		x = call([find_service(), name, "status"])
		if x == 0:
			return True
		return False
	except:
		print >>sys.stderr, "Failed to detect whether %s is running; assuming it is not" % name
		return False

def start_service(service):
	x = call([find_service(), service, "start"])
	if x <> 0:
		print >>sys.stderr, "ERROR: failed to start %s" % service
	time.sleep(1)

def stop_service(service):
	x = call([find_service(), service, "stop"])
	if x <> 0:
		print >>sys.stderr, "ERROR: failed to stop %s" % service

services = [
	"message-switch",
	"forkexecd",
	"xcp-networkd",
	"ffs",
	"xapi",
]

already_started = []
for service in services:
	if is_service_running(service):
		already_started.append(service)

def start():
	for service in services:
		if service not in already_started:
			start_service(service)

def open():
	return XenAPI.xapi_local()

