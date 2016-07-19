#!/usr/bin/env python
import os
import subprocess
import pwd
import sys
import psutil
import time
import logging
import logging.handlers
from procfs import Proc

# Setup logging
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

# Start xstata process in a new process group

try:
  assert len(sys.argv) > 1
except:
  log.critical("Command not passed as an argument? Create a ticket with RCE_Dev")
  sys.exit(1)

cmd = sys.argv[1]

if not os.path.exists(cmd):
  log.critical("{0} does not exist. Check rceapp.yml and create a ticket with RCE_Dev.".format(cmd))
  sys.exit(1)
  
xstata = subprocess.Popen([cmd],
  preexec_fn=os.setsid)

# Get the process group
xstata_pgid = os.getpgid(xstata.pid)

# Wait for the defunct xstata to exit
xstata.wait()

# Get the actual xstata pid
xstata_process = filter(lambda p: p.stat['pgrp'] == xstata_pgid,
  Proc().processes.user(pwd.getpwuid( os.getuid() ).pw_name))

# There should only be one in this pgroup

# Check if there's more than 1. Error differently.
try:
  assert len(xstata_process) < 2
except Exception as e:
  log.critical("More than 1 xstata process found after executing. Create an RCE_Dev ticket with this error.")
  sys.exit(1)

# There must at least be 1
try:
  assert len(xstata_process) == 1
except Exception as e:
  log.critical("No XStata processes running after executing. Did XStata crash upon start? Create an RCE_Dev ticket with this error.")
  sys.exit(1)

# Get the pid
real_xstata_pid = xstata_process[0].stat['pid']

# Sleep until application exits
while psutil.pid_exists(real_xstata_pid):
  time.sleep(1)

sys.exit(0)
