import os
import pwd
import simpleldap
import classad
import htcondor
import hmdccondor.HMDCConstants as CONSTANTS
import re
from datetime import datetime

class HMDCCondor:
  def __init__(self):
    self._collector_batch = htcondor.Collector(CONSTANTS.HMDC_BATCH_HEAD)
    self._collector_int = htcondor.Collector(CONSTANTS.HMDC_INT_HEAD)
    self._batch_schedd = htcondor.Schedd(self._collector_batch.locate(htcondor.DaemonTypes.Schedd))
    self._interactive_schedd = htcondor.Schedd(self._collector_int.locate(htcondor.DaemonTypes.Schedd))

  def submit(self, app_name, app_version, cmd, args, cpu, memory):
    __classad = self._create_classad(
        app_name,
        app_version,
        cmd,
        args,
        cpu,
        memory)

    jobid = self._interactive_schedd.submit(__classad, 1)
    
    # set HMDCApplicationName ClassAd
    # set HMDCApplicationVersion ClassAd

    return jobid

  def poll(self, jobid):
    self.__poll_thread(jobid)
   
  def __poll_thread(self, jobid):
    # loop until the process is running or halted.
    while 1:

      try:
        (my_job_status, my_job) = self.__get_job_status_from_queue(
            jobid)
      except:
        # Job apparently doesn't exist in running queue.
        try:
          (my_job_status, my_job) = self.__get_job_status_from_history(jobid)
        except:
          (my_job_status, my_job) = None, None

      if not my_job_status:
        time.sleep(5)
        continue

      # If value is 1, then we're still negotiating.
      # See http://pages.cs.wisc.edu/~adesmet/status.html
      is_returnable_value = sum(
          map(lambda st: int(st==my_job_status), [2,3,4,5,6])
          ) > 0

      if is_returnable_value:
        return (my_job, my_job_status)
      else:
        # Still in negotiation
        time.sleep(5)
        continue

  def __get_job_status_from_queue(self,jobid):
    job = self._interactive_schedd.query("ClusterId =?= {0}".format(jobid))
    return (int(job[-1]['JobStatus']), job[-1])

  def __get_job_status_from_history(jobid):
    # History returns an iterator, unlike query, so we have to turn it
    # into an array of arrays, which is what the map does.
    job_iterator = self._interactive_schedd.history("ClusterId =?= {0}".
        format(jobid), [''], 1)
    job = map(lambda x: x, job_iterator)[-1]
    job_status = int(job['JobStatus'])
    return (job_status, job)

  def attach(self,jobid):
    return 0

  def __poll_xpra_alive(self,jobid):
    return 0

  def _create_classad(self, app_name, app_version, cmd, cpu, memory, args=None):
    dt = datetime.utcnow().strftime("%Y%m%d%s")
   
    _out = "{0}_{1}".format(app_name, app_version)

    home = pwd.getpwnam(pwd.getpwuid(os.getuid())[0]).pw_dir
    job_dir_base= "{0}/.HMDC/jobs/interactive".format(home)
    job_dir = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt)

    out = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt, '/out.txt')
    err = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt, '/err.txt')

    _classad = classad.ClassAd({
      'HMDCNewSubmit': True,
      'HMDCApplicationName': app_name,
      'HMDCApplicationVersion': app_version,
      'HMDCInteractive': True,
      'HMDCUseXpra': True,
      'JobLeaseDuration': 1200,
      'LocalJobDir': job_dir,
      'HookKeyword': 'LOG',
      'DebugPrepareJobHook': True,
      'Cmd': cmd,
      'Args': args if args else False,
      'RequestMemory': memory,
      'ShouldTransferFiles': 'NO',
      'TransferExecutable': False,
      'TransferIn': False,
      'Out': out,
      'Err': err,
      'Entitlements': self._get_entitlements(),
      'Environment': self._get_environment(),
      'FileSystemDomain': CONSTANTS.FILESYSTEM_DOMAIN
      })

    return _classad

  def _get_entitlements(self):
    # FIXME: Figure out a way to read basedn and uri from openldap
    # configuration, natively.
    _my_username = pwd.getpwuid(os.getuid())[0]

    return ' '.join(
        simpleldap.Connection('directory.hmdc.harvard.edu',encryption='ssl')
        .search("uid={0}".format(_my_username),
          attrs = ['eduPersonEntitlement'], 
          base_dn =
          'dc=login,dc=hmdc,dc=harvard,dc=edu')[-1].values()[-1]) 

  def _get_environment(self):
    return ' '.join(filter(lambda pair: not re.match("^DBUS|^GNOME", pair), map(lambda (x,y): "%s='%s'" %(x,y), os.environ.iteritems())))
