"""A module containing the ``HMDCPoller`` class which facilitates polling
for job statuses"""

import time
import classad
import htcondor
from hmdccondor.HMDCLog import rcelog

class HMDCPoller:
  def __init__(self,id,return_status,schedd):
    """Sets schedd, desired list of JobStatus values, and job id for class.

    :arg id: job id
    :type id: ``int``
    :arg return_status: array of accepted JobStatus values
    :type return_status: ``list``
    :arg schedd: HTCondor Schedd object
    :type schedd: `htcondor.Schedd`

    :Example:

    >>> from htcondor import Schedd
    >>> from hmdccondor import HMDCPoller
    >>> poller = HMDCPoller(73,[0,1,2],Schedd())

    """

    assert isinstance(id, int)
    assert isinstance(return_status, list)
    assert isinstance(schedd, htcondor.Schedd)

    self.id = id
    self.return_status = return_status
    self.schedd = schedd

  def find_job_and_job_status(self):
    """Attempts to find job specified by ``self.id`` either in
    ``self.schedd`` queue or ``self.schedd`` job history.

    :returns: ``(JobStatus, ClassAd)``
    :returns: ``(None, None)``
    :rtype: ``tuple``
    :rtype: ``None``

    :Example:

    >>> from htcondor import Schedd
    >>> from hmdccondor import HMDCPoller
    >>> HMDCPoller(73, [0,1,2], Schedd()).
     find_job_and_job_status()

    """

    def find_job_and_job_status_log_history(f):
      rcelog('critical', "find_job_and_status(): Found job {0} in history. Terminated in error.".
        format(self.id))
      return f

    try:
      return self.__get_job_status_from_queue__()
    except:
      pass

    try:
      return find_job_and_job_status_log_history(self.__get_job_status_from_history__())
    except:
      return (None, None)

  def run(self,id=None):
    """loops until either job with appropriate job status is found or
    returns None. Note this function infinitely loops until result is
    returned. This is best used with a function that tracks time and
    timesout.

    :returns: ``(JobStatus, ClassAd)``
    :returns: ``(None, None)``
    :rtype: tuple

    :Example:
    
    >>> from htcondor import Schedd
    >>> from hmdccondor import HMDCPoller
    >>> HMDCPoller(73, [0,1,2], Schedd()).run()

    """
    # loop until the process is running or halted.
    while 1:

      my_job_status, my_job = self.find_job_and_job_status()

      if not my_job_status:
        time.sleep(5)
        continue

      if sum(map(lambda st: int(st==my_job_status), self.return_status)) > 0:
        return (my_job_status, my_job.printOld())

      time.sleep(5)
      continue

  def __get_job_status_from_queue__(self):
    """returns job status from ``self.schedd`` job queue. raises index
    error if job wasn't found in the queue.

    :returns: ``(JobStatus, ClassAd)``
    :rtype: ``tuple``
    :raises: ``IndexError``

    :Example:

    >>> from htcondor import Schedd
    >>> from hmdccondor import HMDCPoller
    >>> HMDCPoller(73, [0,1,2], Schedd()).
      __get_job_status_from_queue__()

    """

    return (lambda job: (int(job[-1]['JobStatus']),
      job[-1]))(self.schedd.query("ClusterId =?= {0}".format(self.id)))

  def __get_job_status_from_history__(self):
    """returns job status from ``self.schedd`` job history. raises index
    error if job wasn't found in the queue. ``self.schedd.history()``
    returns an interator, unlike query, so we transform it into a
    two-dimensional array using ``map()``

    :returns: ``(JobStatus, ClassAd)``
    :rtype: ``tuple``
    :raises: ``IndexError``

    :Example:

    >>> from htcondor import Schedd
    >>> from hmdccondor import HMDCPoller
    >>> HMDCPoller(73, [0,1,2], Schedd()).
      __get_job_status_from_history__()

    """

    # History returns an iterator, unlike query, so we have to turn it
    # into an array of arrays, which is what the map does.

    return (lambda job: (int(job['JobStatus']), job))(
        map(lambda x: x, self.schedd.history("ClusterId =?= {0}".
          format(self.id), [''], 1))[-1])
