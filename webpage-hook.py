#!/usr/bin/python

"""
CGI script to take a bitbucket payload triggered when a user pushes to the
natcap bitbucket repository https://bitbucket.org/natcap/invest-natcap.webpage.

When triggered, this script will cause the source of the static site at
http://naturalcapitalproject.org/ to be updated to the tip revision of the
webpage repository.
"""

import cgitb
import os
import json
import time
import sys
import subprocess

cgitb.enable(display=0, logdir=".")

print "Content-Type: text/html" # HTML is following
print # blank line, end of headers

REPOSITORY_PATH = 'https://bitbucket.org/natcap/invest-natcap.webpage'
REPOSITORY_DIR = os.path.expanduser('~/invest-natcap.webpage/')
with open('webpage-hook.log', 'a') as LOG_FILE:
    NULL_FH = open("NUL", "w")
    try:
        HOOK_DATA = json.loads(sys.stdin.read())
        if HOOK_DATA['repository']['links']['html']['href'] == REPOSITORY_PATH:
            if not os.path.isdir(REPOSITORY_DIR):
                subprocess.call(
                    ["hg", "clone", REPOSITORY_PATH, REPOSITORY_DIR],
                    stdout=NULL_FH, stderr=NULL_FH)
            else:
                # making explicit call to bitbucket path (set in REPO/.hg/hgrc)
                # for now.
                subprocess.call(
                    ["hg", "pull", "bitbucket", "--repository", REPOSITORY_DIR],
                    stdout=NULL_FH, stderr=NULL_FH)
            subprocess.call(
                ["hg", "up", "-C", "--repository", REPOSITORY_DIR],
                stdout=NULL_FH, stderr=NULL_FH)
            LOG_FILE.write("[%s] successfuly updated\n" % time.strftime("%c"))

    except Exception as exception:
        LOG_FILE.write(
            "[%s] Exception\n%s\n" % (time.strftime("%c"), str(exception)))
        LOG_FILE.flush()
    NULL_FH.close()
