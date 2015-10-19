import classad

class RCEJobNotFoundError(Exception):
  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('No job running, held, or terminated with jobid {0}'.
        format(self.jobid))

class RCEJobTookTooLongStartError(Exception):
  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('Job {0} took too long to start'.
        format(self.jobid))

class RCEXpraTookTooLongStartError(Exception):
  def __init__(self, ad):
    self.ad = ad
  def __get_err__(self):
    return ad['Err'].eval()
  def __get_application_name__(self):
    return ad['HMDCApplicationName']
  def __get_application_version__(self):
    return ad['HMDCApplicationVersion']
  def __str__(self):
    return repr('Job {0}, xpra server took too long to start'.
        format(int(ad['ClusterId'])))
