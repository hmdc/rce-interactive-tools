import os
import pwd
import simpleldap
import classad
import htcondor
import hmdccondor.HMDCConstants as CONSTANTS
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

  def poll(jobid):
    return 0

  def _create_classad(self, app_name, app_version, cmd, cpu, memory, args=None):
    dt = datetime.utcnow().strftime("%Y%m%d%s")

    _classad = classad.ClassAd({
      'HMDCApplicationName': app_name,
      'HMDCApplicationVersion': app_version,
      'HMDCInteractive': True,
      'HMDCUseXpra': True,
      'Cmd': cmd,
      'Args': args if args else False,
      'RequestMemory': memory,
      'ShouldTransferFiles': 'NO',
      'TransferExecutable': False,
      'TransferIn': False,
      'Out': '{0}_{1}_{2}.out.txt'.format(app_name, app_version, dt),
      'Err': '{0}_{1}_{2}.err.txt'.format(app_name, app_version, dt),
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
    return ' '.join(map(lambda (x,y): "%s='%s'" %(x,y), os.environ.iteritems()))
