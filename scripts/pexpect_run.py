#!/usr/bin/python
import sys
import pexpect

_logfile = sys.argv[1]

try:
  with open(_logfile, 'w+') as _logfile_fd:
    pexpect.run(' '.join(sys.argv[2:]), logfile=_logfile_fd)
except:
  sys.exit(1)

sys.exit(0)
