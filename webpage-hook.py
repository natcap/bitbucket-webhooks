#!/usr/bin/python

"""
CGI script to take a bitbucket payload triggered when a user pushes to the
natcap bitbucket repository https://bitbucket.org/natcap/invest-natcap.webpage.

When triggered, this script will cause the source of the static site at
http://naturalcapitalproject.org/ to be updated to the tip revision of the
webpage repository.
"""

import os
import json
import time
import sys

REPOSITORY_PATH = 'https://bitbucket.org/natcap/invest-natcap.webpage'
REPOSITORY_DIR = os.path.expanduser('~/invest-natcap.webpage/')
with open('webpage-hook.log', 'a') as LOG_FILE:
    NULL_FH = open("NUL", "w")
    try:
        HOOK_DATA = json.loads(sys.stdin.read())
        LOG_FILE.write("New hook data: %s" % json.dumps(HOOK_DATA, indent=4, sort_keys=True))

    except Exception as exception:
        LOG_FILE.write(
            "[%s] Exception\n%s\n" % (time.strftime("%c"), str(exception)))
        LOG_FILE.flush()
    NULL_FH.close()
