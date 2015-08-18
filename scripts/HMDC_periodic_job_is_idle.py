#!/usr/bin/env python2.6
import sys
import classad
import htcondor
import logging
import logging.handlers
from hmdccondor import HMDCCondor
# Import classad

# Setup logging
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

def update_job(condor, clusterid, jobid, is_job_idle):

  try:
    schedd, classad = condor.get_sched_for_job(jobid)
  except:
    log.critical('Job {0}: Could not find ClassAd'.format(jobid))
    return 0

  log.info('Job {0}: Found ClassAd.'.format(jobid))

  q_classad = classad[0]

  try:
    current_time = int(q_classad['CurrentTime'].eval())
  except:
    log.critical(
        'Job {0}: Could not evaluate CurrentTime'.format(jobid)
        )
    return 0

  log.info('Job {0}: CurrentTime = {1}'.format(jobid, current_time))

  try:
    last_check_time = int(q_classad['LastIdleCheckTime'])
    idle_time = int(q_classad['JobCpuIdleTime'])
  except KeyError:
    last_check_time = 0
    idle_time = 0
  except:
    return 0

  log.info('Job {0}: \
last_check_time={1},current_time={2},idle_time={3}'.format(jobid,
        last_check_time,
        current_time,
        idle_time))

  if is_job_idle:
    differend = current_time - last_check_time
    idle_time += differend if last_check_time > 0 else 0
  else:
    idle_time = 0

  try:
    schedd.edit([jobid], 'LastIdleCheckTime', str(current_time))
    schedd.edit([jobid], 'JobCpuIdleTime', str(idle_time))
  except:
    log.critical('Job {0}: Unable to edit ClassAd in queue'.format(
      jobid))
    return 0

  log.info('Job {0}: LastIdleCheckTime={1}, JobCpuIdleTime={2}'.format(
    jobid,
    current_time,
    idle_time))

  return 0


def main():
  
  hmdc_condor = HMDCCondor()

  int_collect = hmdc_condor._collector

  job_classad = classad.parseOld(sys.stdin)

  try:
    is_interactive = job_classad['HMDCInteractive']
  except:
    sys.exit(0)

  if is_interactive == False:
    sys.exit(0) 

  
  # If the job isn't currently running, we don't care.
  if job_classad['JobStatus'] != 2:
    job.info('Job is no longer running, exiting.')
    return 0

  clusterid = job_classad['ClusterId']
  procid = job_classad['ProcId']

  log.info ('Job {0}.{1}: Running.'.format(clusterid, procid))

  jobid = "{0}.{1}".format(
      str(clusterid),
      str(procid))

  try:
    is_job_idle = int_collect.query(htcondor.AdTypes.Any,
        'JobId =?= "{0}"'.format(jobid),
        ['JobCpuIsIdle'])[0]['JobCpuIsIdle'].eval()

    log.info('Job {0}: Idle? {1}'.format(jobid, is_job_idle))

  except:
    log.info('Job {0}: Unable to evaluate JobCpuIsIdle')
    return 0

  return update_job(hmdc_condor,
      clusterid,
      jobid,
      is_job_idle)

if __name__ == '__main__':
  v = main()
  exit(v)
