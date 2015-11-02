from tabulate import tabulate
from hmdccondor import HMDCCondor
from hmdccondor import RCEJobNotFoundError, \
  RCEJobTookTooLongStartError, \
  RCEXpraTookTooLongStartError, \
  RCEJobDidNotStart, \
  rcelog
from ProgressBarThreadCli import ProgressBarThreadCli
import argparse
import rceapp
import logging
import logging.handlers


class RCEConsoleClient:
    def __init__(self, rceapps, application=None, version=None, memory=None, cpu=None):
        self.rceapps = rceapps
        self.application = application
        self.version = version
        self.memory = memory
        self.cpu = cpu
        return

    def attach_all(self):
        return map(lambda ad: self.attach_app(int(ad['ClusterId'])), HMDCCondor().get_my_jobs())

    def attach_app(self, jobid, ad=None):
        try:
          return HMDCCondor().attach(jobid, self.rceapps, ad=ad)
        except RCEJobNotFoundError as e:
          rcelog('critical', "attach_app(): Job {0} not found.".format(e.jobid))
          print e.message()  
          return 1
        except Exception as e:
          rcelog('critical', "attach_app(): Unkown exception: {0}".format(e))
          print """
          Encountered unknown exception. Please report this to
          support@help.hmdc.harvard.edu with the following exception data:

          Exception: {0}
          """.format(e)
          return 1

    def munge_requested_resources(self, label, version):

      def __resource_none_or_not_adjustable__():
        if getattr(self, label) is None:
          return True

        if self.rceapps.supports_adjustable(self.application, label):
          return False
        else:
          print "** {0} unable to use {1} greater than default".format(
              self.application, label)
          print "** Using default {0} value for {1}".format(
              label, self.application)
          return True

        return False

      return (getattr(self.rceapps, label))(self.application, 
          version) if __resource_none_or_not_adjustable__() else \
              getattr(self, label)

    def run_app(self):
        _version = self.version if self.version else \
                self.rceapps.get_default_version(self.application)

        # else:
        #  print 'Application {0} does not exist.'.format(application)
        #  print 'Run rce_submit.py -l to view a list of available applications.'
        #  return 1

        rce = HMDCCondor()

        _cpu = self.munge_requested_resources('cpu', _version)
        _memory = self.munge_requested_resources('memory', _version)

        # _cpu = self.rceapps.cpu(self.application, _version) if \
        #        self.cpu is None else self.cpu

        # _memory = self.rceapps.memory(self.application,_version) if \
        #        self.memory is None else self.memory


        job_submit_bar = ProgressBarThreadCli('* Submitting job')
        job_submit_bar.start()
 
        job = rce.submit(
            self.application,
            _version,
            self.rceapps.command(self.application,_version),
            self.rceapps.args(self.application,_version),
            _memory,
            _cpu)

        job_submit_bar.stop()
        job_submit_bar.join()

        job_wait_bar = ProgressBarThreadCli('* Waiting for job to start')
        job_wait_bar.start()

        try:
          job_status, ad = rce.poll(job, use_local_schedd=True)
        except RCEJobTookTooLongStartError as e:
          try:
            job_wait_bar.stop()
            job_wait_bar.join()
          except:
            pass

          rcelog('critical', 'run_app(): Job {0} took too long to start: Application={1},Version={2},RequestMemory={3},RequestCpu={4}'.
            format(job, self.application, _version, _memory, _cpu))

          print e.message()

          return 1
        except RCEJobDidNotStart as e:
          try:
            job_wait_bar.stop()
            job_wait_bar.join()
          except:
            pass

          rcelog('critical', 'run_app(): Job {0} did not start. Reason: {1}'.format(job, e))

          print e.message()
          return 1
        except Exception as e:
          try:
            job_wait_bar.stop()
            job_wait_bar.join()
          except:
            pass

          rcelog('critical', "run_app(): Unknown exception: {0}".format(e))

          print """
          Application encountered unexpected exception while polling for Job
          {0} to start. Please notify support@help.hmdc.harvard.edu and
          include the following exception output.

          Exception: {1}
          """.format(job, e)

          return 1

        job_wait_bar.stop()
        job_wait_bar.join()

        job_xpra_wait_bar = ProgressBarThreadCli("* Attaching to job {0}".
            format(job))
        job_xpra_wait_bar.start()

        try:
          xpra_client_pid = self.attach_app(job, ad=ad)
        except RCEXpraTookTooLongStartError as e:
          try:
            job_xpra_wait_bar.stop()
            job_xpra_wait_bar.join()
          except:
            pass

          rcelog('critical', "run_app(): Job {0}, xpra took too long to start. Printing classad.".format(job))
          rcelog('critical', e.get_ad())
          print e.message()

          return 1
        except Exception as e:
          try:
            job_xpra_wait_bar.stop()
            job_xpra_wait_bar.join()
          except:
            pass

          rcelog('critical', "run_app(): Encountered unknown exception: {0}".format(e))

          print """
          Application encountered unexpected exception while attempting to
          attach to job {0}. Please notify support@help.hmdc.harvard.edu and
          include the following exception output.

          Exception: {1}
          """.format(job, e)

          return 1

        job_xpra_wait_bar.stop()
        job_xpra_wait_bar.join()

        return xpra_client_pid


