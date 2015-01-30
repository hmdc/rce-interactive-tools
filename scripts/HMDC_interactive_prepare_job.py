#!/usr/bin/python
import sys
import classad
import os
import pwd
from datetime import datetime
# Import classad

__BASENAME__ = os.path.basename(__file__)


# Quick and dirty debug function, please replace.
def debug(will_debug, _fd, message): 
  if will_debug:
    dt = datetime.utcnow().strftime("%Y%m%d %s")
    _fd.write("[{0}] {1}\n".format(dt, message))
    return True
  else:
    return False

job_classad = classad.parseOld(sys.stdin)
home = pwd.getpwnam(pwd.getpwuid(os.getuid())[0]).pw_dir

# Should we debug this hook?
try:
  _debug = job_classad['DebugPrepareJobHook']
except:
  _debug = False

clusterid = job_classad['ClusterId']
timestamp = job_classad['LastMatchTime']
host = job_classad['RemoteHost'].split('@')[-1]

DEBUG_LOG = None
DEBUG_LOG_BASE_PRIMARY = "{0}/.HMDC/jobs/debug/{1}.{2}.log".format(home,
    __BASENAME__, clusterid)
DEBUG_LOG_BASE_ALTERNATE = "/tmp/{0}.{1}.log".format(__BASENAME__,clusterid)

try:
  debug_fd = open(DEBUG_LOG_BASE_PRIMARY,'w+') if _debug else None
  DEBUG_LOG = DEBUG_LOG_BASE_PRIMARY
except:
  debug_fd = open(DEBUG_LOG_BASE_ALTERNATE,'w+') if _debug else None
  DEBUG_LOG = DEBUG_LOG_BASE_ALTERNATE

debug(_debug, debug_fd,
    "Got ClassAd with clusterid={0},LastMatchTime={1},RemoteHost={2}".
    format(clusterid,timestamp,host))

try:
  application = job_classad['HMDCApplicationName']
  application_version = job_classad['HMDCApplicationVersion']
except:
  application = '_'.join(job_classad['OrigCmd'].split('/'))
  application_version = None

debug(_debug, debug_fd,
    "ClassAd application is {0}, version {1}.".format(
      application, str(application_version)))

job_dir = job_classad['LocalJobDir'].eval()

debug(_debug, debug_fd,
    "{0} will create directory {1}".format(__BASENAME__,job_dir))

try:
  os.mkdir(job_dir, 0755)
  debug(_debug, debug_fd,
      "Successfully created directory: {0}".format(job_dir))
except Exception as e:
  debug(_debug, debug_fd,
      "Encountered exception when running os.mkdir, continuing anyway: {0}".format(
        e))


debug(_debug, debug_fd, 
    "Writing the following modified ClassAd to stdout")
debug(_debug, debug_fd,
    job_classad.printOld())

sys.stdout.write (job_classad.printOld())

if debug_fd:
  try:
    debug(_debug,debug_fd, 
        "Closing file descriptor to {0}".format(DEBUG_LOG))
    debug_fd.close()
  except:
    debug(_debug,debug_fd,
        "Encountered exception closing file descriptor to {0}".format(
          DEBUG_LOG))
    raise

sys.exit(0)
