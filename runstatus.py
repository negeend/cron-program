#!/usr/bin/env python3
# -*- coding: ascii -*-

import sys, os, time, signal

pidfile = os.path.expanduser("runner.pid")
statusfilename = "runner.status"

try:
    file = open(pidfile, 'r')
    pid = file.readline()
    file.close()
except FileNotFoundError:
    sys.stderr.write("file {} not found".format(pidfile) + "\n")
    sys.exit()

try:
    os.kill(int(pid), signal.SIGUSR1) 
except OSError:
    sys.stderr.write("signal failed - invalid PID\n")
    sys.exit()

try:    
    file = open(statusfilename, 'r')
except FileNotFoundError:
    sys.stderr.write("file {} not found".format(statusfilename) + "\n")
    sys.exit()


i = 0
counter = 0
while i < 5:
    if os.path.getsize(statusfilename) == 0:
        counter += 1
        time.sleep(1)
    else:
        break
    i += 1
    
if counter == 5:
    sys.stderr.write("status timeout\n")
    sys.exit()
 
file = open(statusfilename, 'r')
lines = file.readlines()
for status in lines:
    print(status.strip())
file.close()


file = open(statusfilename, 'w')
file.close()