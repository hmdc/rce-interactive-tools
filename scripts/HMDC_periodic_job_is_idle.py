#!/usr/bin/python
import sys
import classad
import htcondor
from hmdccondor import HMDCCondor
# Import classad


def update_job(schedd, clusterid, jobid, is_job_idle):
  try:
    q_classad = schedd.query('ClusterId =?= {0}'.format(clusterid))[0]
  except:
    return 0

  print '[DEBUG] in update_job, found ClassAd for {0}'.format(jobid)

  try:
    current_time = int(q_classad['CurrentTime'].eval())
  except:
    return 0

  print '[DEBUG] {0} CurrentTime = {1}'.format(jobid, current_time)

  try:
    last_check_time = int(q_classad['LastIdleCheckTime'])
    idle_time = int(q_classad['JobCpuIdleTime'])
  except KeyError:
    last_check_time = 0
    idle_time = 0
  except:
    return 0

  print '[DEBUG]\
 {0},last_check_time={1},current_time={2},idle_time={3}'.format(jobid,
      last_check_time,
      current_time,
      idle_time)
 
  if is_job_idle:
    differend = current_time - last_check_time
    idle_time += differend if last_check_time > 0 else 0
  else:
    idle_time = 0

  try:
    schedd.edit([jobid], 'LastIdleCheckTime', str(current_time))
    schedd.edit([jobid], 'JobCpuIdleTime', str(idle_time))
    print '[DEBUG] SET {0} : LastIdleCheckTime={1},JobCpuIdleTime={2}'.format(
      jobid,
      current_time,
      idle_time,
      )
  except:
    return 0

  return 0


def main():
  hmdc_condor = HMDCCondor()
  schedd = hmdc_condor._interactive_schedd
  int_collect = hmdc_condor._collector_int

  job_classad = classad.parseOld(sys.stdin)

  # If the job isn't currently running, we don't care.
  if job_classad['JobStatus'] != 2:
    return 0

  clusterid = job_classad['ClusterId']
  procid = job_classad['ProcId']

  print '[DEBUG] {0}.{1} is running.'.format(clusterid, procid)

  jobid = "{0}.{1}".format(
      str(clusterid),
      str(procid))

  try:
    is_job_idle = int_collect.query(htcondor.AdTypes.Any,
        'JobId =?= "{0}"'.format(jobid),
        ['JobCpuIsIdle'])[0]['JobCpuIsIdle'].eval()

    print '[DEBUG] {0} is idle? {1}'.format(jobid, is_job_idle)

  except:
    return 0

  return update_job(schedd,
      clusterid,
      jobid,
      is_job_idle)

if __name__ == '__main__':
  v = main()
  exit(v)
