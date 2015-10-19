class RCEJobNotFoundError(Exception):
  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('No job running, held, or terminated with jobid {0}'.
        format(self.jobid))
