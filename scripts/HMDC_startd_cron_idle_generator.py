#!/usr/bin/env python2.6
import htcondor
import classad
import sys
import os
import stat
from glob import glob

def generate_string(dir):

  def get_jobid_idle_string(ad):
    return "{0}.{1},{2}".format(ad['ClusterId'], ad['ProcId'], get_idle_time())

  def get_idle_time():
    try:
      with open("{0}/.idletime".format(dir)) as f:
        return f.readline().rstrip()
    except:
      return 0

  return get_jobid_idle_string(classad.parseOne(open("{0}/.job.ad".format(dir))))

if not "STARTD" in htcondor.param.get("DAEMON_LIST"):
  sys.exit(0)

try:
  with open(htcondor.param.get("STARTD_CRON_IDLEJOBS_EXECUTABLE"), 'w') as f:
    f.write("""#!/bin/sh
cat <<EOF
HMDCIdleJobs = \"{0}\"
EOF""".format(' '.join(map(generate_string, glob("{0}/dir_*".format(htcondor.param.get('EXECUTE')))))))
    os.fchmod(f.fileno(), stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH | stat.S_IRWXU | stat.S_IROTH )
except Exception as e:
  sys.exit(0)
