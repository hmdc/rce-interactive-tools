import os
import pwd
import simpleldap
import classad
import htcondor
import hmdccondor.HMDCConstants as CONSTANTS
import hmdccondor.HMDCPoller
import re
import time
import multiprocessing as mp
import copy
from datetime import datetime

def poll_thread(id,return_status):
  schedd = HMDCCondor()._interactive_schedd

  poller = hmdccondor.HMDCPoller(id,return_status,schedd)
 
  return poller.run()

class HMDCCondor:
  def __init__(self):
    self._collector_batch = htcondor.Collector(CONSTANTS.HMDC_BATCH_HEAD)
    self._collector_int = htcondor.Collector(CONSTANTS.HMDC_INT_HEAD)
    self._batch_schedd = htcondor.Schedd(self._collector_batch.locate(htcondor.DaemonTypes.Schedd))
    self._interactive_schedd = htcondor.Schedd(self._collector_int.locate(htcondor.DaemonTypes.Schedd))
    self._return_status = [
      CONSTANTS.JOB_STATUS_RUNNING,
      CONSTANTS.JOB_STATUS_REMOVED,
      CONSTANTS.JOB_STATUS_COMPLETED,
      CONSTANTS.JOB_STATUS_HELD,
      CONSTANTS.JOB_STATUS_SUBMIT_ERR]
    self.POLL_TIMEOUT = 90

  def submit(self, app_name, app_version, cmd, args, cpu, memory):
    __classad = self._create_classad(
        app_name,
        app_version,
        cmd,
        args,
        cpu,
        memory)

    jobid = self._interactive_schedd.submit(__classad, 1)
    
    return jobid

  def poll(self, jobid, return_status=None):
    _return_status = return_status if return_status else self._return_status

    # start a thread so we can timeout on polling.
    pool = mp.Pool(1)
    result = pool.apply_async(poll_thread, (jobid, _return_status))
    pool.close()

    try:
      return result.get(self.POLL_TIMEOUT) 
    except:
      pool.terminate()
      raise
   
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
