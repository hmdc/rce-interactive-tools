import classad

class RCEJobNotFoundError(Exception):
  """RCEJobNotFoundError is thrown when a user attempts to attach a job
  with a jobid that does not exist."""

  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('No job running, held, or terminated with jobid {0}'.
        format(self.jobid))
  def message(self):
    """message returns the explanatory text for RCEJobNotFoundError.

    :returns: text
    :rtype: str

    """

    return """\
Job {0} could not be attached. This job could not be found on the
RCE. Are you sure this is the correct job id? Run the following
command to determine your currently running jobs on the RCE.

rce_submit.py -jobs\
""".format(self.jobid)

class RCEJobDidNotStart(Exception):
  """RCEJobDidNotStart is thrown when a user submits a job but it fails
  to start."""

  def __init__(self, result):
    self.status = result[0]
    self.ad = classad.parseOld(result[1])
  def __str__(self):
    return repr('Job {0} did not start properly. Return status: {1}'.
      format(int(self.ad['ClusterId']), self.ad['JobStatus']))
  def __determine_cause__(self):
    """__determine_cause__() returns the reason why the job did not
    start, which is embedded in the ClassAd held by the exception.

    :returns: reason for job start failure
    :rtype: str

    """
    try:
      return "HoldReason={0}".format(self.ad['HoldReason'])
    except:
      pass

    try:
      return "RemoveReason={0}".format(self.ad['RemoveReason'])
    except:
      pass

    try:
      return "Job completed prematurely: {0}".format(self.ad['CompletionDate'])
    except:
      return "Unknown reason"
  def message(self):
    """returns explanatory text as to why job did not start.

    :returns: text
    :rtype: str

    """

    return """\
Your job {0} exited before launching {1}. This indicates that one
of the following conditions are present:

* Your application crashed immediately upon execution.
* You allocated an improper amount of memory and/or CPU.
* An internal problem with the RCE.

According to your job's ClassAd, your job exited due to the following
reason: 

{2}

For more information, run:

condor_history -l {0}

or email support@help.hmdc.harvard.edu\
""".format(self.ad['ClusterId'], self.ad['HMDCApplicationName'], self.__determine_cause__())

class RCEJobTookTooLongStartError(Exception):
  """RCEJobTookTooLongStartError is thrown when a user submits a job but
  it takes too long to start."""

  def __init__(self, jobid):
    self.jobid = jobid
  def __str__(self):
    return repr('Job {0} took too long to start'.
        format(self.jobid))
  def message(self):
    """returns explanatory text to user.

    :returns: text
    :rtype: str

    """

    return """\
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
automatically remove this job.\
""".format(self.jobid)

class RCEXpraTookTooLongStartError(Exception):
  """RCEXpraTookTooLongStartError is thrown if the xpra server, running
  on an HTCondor worker node, takes too long to start under the
  submitted job's slot."""

  def __init__(self, ad):
    self.ad = ad
  def get_ad(self):
    """A getter that returns the ClassAd of the failed job stored in the
    exception.

    :returns: classad of failed job
    :rtype: classad.ClassAd

    """

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
    """returns explanatory text wrt. xpra taking too long to start,
    advises contacting support as this is a critical error.

    :returns: text
    :rtype: str

    """
    return """\
Job {0}, {1} {2}, was unable to start Xpra. This is a critical
error. Please send an email to support@help.hmdc.harvard.edu and
include the contents of the following file:
{3}\
""".format(
         self.jobid,
         self.__get_application_name__(),
         self.__get_application_version__(),
         self.__get_err__())
