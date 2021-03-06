"""
Useful constants for HTCondor.
"""

import htcondor

FILESYSTEM_DOMAIN = htcondor.param.get("FILESYSTEM_DOMAIN")
CONDOR_HOST = htcondor.param.get("CONDOR_HOST")
JOB_STATUS_IDLE = 1
JOB_STATUS_RUNNING = 2
JOB_STATUS_REMOVED = 3
JOB_STATUS_COMPLETED = 4
JOB_STATUS_HELD = 5
JOB_STATUS_SUBMIT_ERR = 6
