import htcondor
import hmdccondor.constants as HMDC_Constants

class HMDCCondor:
  def __init__(self):
    _collector_batch = htcondor.Collector(HMDC_Constants.HMDC_BATCH_HEAD)
    _collector_int = htcondor.Collector(HMDC_Constants.HMDC_INT_HEAD)
    _batch_schedd = htcondor.Schedd(_collector_batch.locate(htcondor.DaemonTypes.Schedd))
    _interactive_schedd = htcondor.Schedd(_collector_int.locate(htcondor.DaemonTypes.Schedd))

  def submit(self, app_name, app_version, cmd, args, cpu, memory):
    # set HMDCApplicationName ClassAd
    # set HMDCApplicationVersion ClassAd
    return 0

  def poll(jobid):
    return 0

  def _create_classad(self, cmd, args, cpu, memory):
    return 0
