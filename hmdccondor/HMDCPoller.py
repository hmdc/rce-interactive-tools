import time
import classad

class HMDCPoller:
  def __init__(self,id,return_status,schedd):
    self.id = id
    self.return_status = return_status
    self.schedd = schedd

  def run(self,id=None):
    # loop until the process is running or halted.
   
    if id:
      self.id = id
 
    jobid = self.id
    return_status = self.return_status
    
    while 1:

      try:
        (my_job_status, my_job) = self.__get_job_status_from_queue()
      except:
        # Job apparently doesn't exist in running queue.
        try:
          (my_job_status, my_job) = self.__get_job_status_from_history()
        except:
          (my_job_status, my_job) = None, None

      if not my_job_status:
        time.sleep(5)
        continue

      # If value is 1, then we're still negotiating.
      # See http://pages.cs.wisc.edu/~adesmet/status.html
      is_returnable_value = sum(
          map(lambda st: int(st==my_job_status), return_status)
          ) > 0

      if is_returnable_value:
        return (my_job_status, my_job.printOld())
      else:
        # Still in negotiation
        time.sleep(5)
        continue

  def __get_job_status_from_queue(self):
    jobid = self.id
    job = self.schedd.query("ClusterId =?= {0}".format(jobid))
    return (int(job[-1]['JobStatus']), job[-1])

  def __get_job_status_from_history(self):
    jobid = self.id
    # History returns an iterator, unlike query, so we have to turn it
    # into an array of arrays, which is what the map does.
    job_iterator = self.schedd.history("ClusterId =?= {0}".
        format(jobid), [''], 1)
    job = map(lambda x: x, job_iterator)[-1]
    job_status = int(job['JobStatus'])
    return (job_status, job)

 
