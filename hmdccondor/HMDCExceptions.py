import classad

class RCEJobNotFoundError(Exception):
  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('No job running, held, or terminated with jobid {0}'.
        format(self.jobid))
  def message(self):
    return """
    Job {0} could not be attached. This job could not be found on the
    RCE. Are you sure this is the correct job id? Run the following
    command to determine your currently running jobs on the RCE.
        rce_submit.py -jobs
    """.format(self.jobid)

class RCEJobTookTooLongStartError(Exception):
  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('Job {0} took too long to start'.
        format(self.jobid))
  def message(self):
    return """
    Your job {0} took too long to start. Typically, an RCE job should
    take between thirty seconds and one minute to start, unless the
    following conditions are present:

    * The RCE cluster is saturated and can no longer accept any more
      jobs. Run 'rce-info.sh' to determine if any free space on the
      cluster is available.
    * You asked for too much memory or cpu. Run the following command
      to determine if your requested memory or cpu allocation is too
      large:
        condor_q -analyze {0}
    * Your job suddenly terminated and/or something is wrong with the
      RCE. If you're unable to determine why your job failed to start,
      send an e-mail to support@help.hmdc.harvard.edu.

    Job {0} will remain in the queue for ten minutes. If job {0} is
    unable to match a resource after ten minutes, the RCE will
    automatically remove this job.
    """.format(self.jobid)

class RCEXpraTookTooLongStartError(Exception):
  def __init__(self, ad):
    self.ad = ad
  def get_ad(self):
    return self.ad
  def __get_err__(self):
    return ad['Err'].eval()
  def __get_application_name__(self):
    return ad['HMDCApplicationName']
  def __get_application_version__(self):
    return ad['HMDCApplicationVersion']
  def __str__(self):
    return repr('Job {0}, xpra server took too long to start'.
        format(int(ad['ClusterId'])))
  def message(self):
    return """
    Job {0}, {1} {2}, was unable to start Xpra. This is a critical
    error. Please send an email to support@help.hmdc.harvard.edu and
    include the contents of the following file:
    {3}
    """.format(
            self.jobid,
            self.__get_application_name__(),
            self.__get_application_version__(),
            self.__get_err__())
