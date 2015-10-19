import time
import classad
import htcondor
from hmdccondor import HMDCLog

class HMDCPoller:
  def __init__(self,id,return_status,schedd):

    assert isinstance(id, int)
    assert isinstance(return_status, list)
    assert isinstance(schedd, htcondor.Schedd)

    self.id = id
    self.return_status = return_status
    self.schedd = schedd
    self.log = (HMDCLog(__name__)).log

  def find_job_and_job_status(self):
    try:
      self.log.debug("Attempting to get job {0} classad from queue".
          format(self.id))
      return self.__get_job_status_from_queue__()
    except:
      self.log.debug("Job {0} is not in queue; try history.".format(self.id))
      pass

    try:
      self.log.debug("Attempting to get job {0} classad from history".
          format(self.id))
      return self.__get_job_status_from_history__()
    except:
      self.log.debug("Job {0} is neither in queue nor history".
          format(self.id))
      return (None, None)

  def run(self,id=None):
    # loop until the process is running or halted.
    while 1:

      my_job_status, my_job = self.find_job_and_job_status()

      if not my_job_status:
        self.log.debug("Job {0}'s job status is {1}. Keep polling".
            format(self.id, my_job_status))
        time.sleep(5)
        continue

      if sum(map(lambda st: int(st==my_job_status), self.return_status)) > 0:
        self.log.debug("Job {0}'s job status is {1}. Returning".
            format(self.id, my_job_status))
        return (my_job_status, my_job.printOld())

      time.sleep(5)
      continue

  def __get_job_status_from_queue__(self):
    return (lambda job: (int(job[-1]['JobStatus']),
      job[-1]))(self.schedd.query("ClusterId =?= {0}".format(self.id)))

  def __get_job_status_from_history__(self):
    # History returns an iterator, unlike query, so we have to turn it
    # into an array of arrays, which is what the map does.

    return (lambda job: (int(job['JobStatus']), job))(
        map(lambda x: x, self.schedd.history("ClusterId =?= {0}".
          format(self.id), [''], 1))[-1])
