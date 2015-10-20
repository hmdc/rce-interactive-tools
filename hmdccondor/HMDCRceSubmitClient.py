from tabulate import tabulate
from hmdccondor import HMDCCondor
from hmdccondor import RCEJobNotFoundError, \
  RCEJobTookTooLongStartError, \
  RCEXpraTookTooLongStartError
from ProgressBarThreadCli import ProgressBarThreadCli
import argparse
import rceapp
import logging
import logging.handlers

class HMDCRceSubmitClient:
  def __init__(self):
    return None

  def __parse_args(self):
    parser = argparse.ArgumentParser(
        description = 'RCE interactive job submission and access tool'
        )

    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables verbose output.')

    parser.add_argument('-c', '--config',
        help='Path to rce app configuration yml (e.g.:\
        /usr/local/HMDC/etc/rceapp.yml',
        nargs='?',
        const='/etc/rceapp.yml',
        default='/etc/rceapp.yml',
        type=str,
        )

    parser.add_argument('-l', '--list', action='store_true',
        help='List supported RCE applications and versions.'
        )

    parser.add_argument('-r', '--run', action='store_true',
        help='Run a job'
        )

    parser.add_argument('-a', '--app',
        help='App to run on the RCE Cluster.'
        )

    parser.add_argument('-memory', '--memory',
        type=int,
        help='Amount of memory to request for job (in GB)',
        default=None
        )

    parser.add_argument('-cpu', '--cpu',
        type=int,
        help='Number of CPUs to request for job.',
        default=None
        )

    parser.add_argument('-v', '--version', 
        help='Version of app to run on the RCE cluster'
        )

    parser.add_argument('-nogui', '--nogui', action='store_true',
        help='Set this if you want to run the app without a GUI'
        )

    parser.add_argument('-attachall', '--attachall',
        action='store_true',
        help='Attach all running graphical jobs',
        default=False)

    parser.add_argument('-attach', '--attach',
        type=int,
        help='Takes a JobID as an argument. Accesses a running job.'
        )

    parser.add_argument('-jobs', '--jobs', action='store_true',
        help='Lists running jobs'
        )

    return parser.parse_args()


  def __version_string(self, app, version):
    rceapps = self.rceapps
    if rceapps.is_default(app,version):
      return "%s **" %(version)
    else:
      return version

  def __list_apps(self):

    rceapps = self.rceapps

    table = []
    _apps = sorted(rceapps.apps(), key=lambda s: s.lower())

    for app in _apps:
      _versions = rceapps.versions(app)
      
      table.append([app, 
        self.__version_string(app, _versions.pop())])

      map(lambda v: table.append(
        ['', self.__version_string(app, v)]),
          _versions)

    return tabulate(table, headers=['Application', 'Version(s)'])

  def __list_jobs(self):
    return tabulate(map(
      lambda ad: [float(ad['ClusterId']),
        ad['HMDCApplicationName'],
        ad['HMDCApplicationVersion'],
        ad['RequestCpus'],
        ad['RequestMemory']],
      HMDCCondor().get_my_jobs()),
      headers=['Job Id', 
        'Application', 
        'Version', 
        'Requested Cpus', 
        'Requested Memory'])

  def list_jobs(self):
    print self.__list_jobs()

  def list_apps(self):
    print "** denotes default"
    print self.__list_apps()

  def attach_all(self):
    return map(lambda ad: self.attach_app(int(ad['ClusterId'])), HMDCCondor().get_my_jobs())

  def attach_app(self, jobid, ad=None):
    try:
      return HMDCCondor().attach(jobid, self.rceapps, ad=ad)
    except RCEJobNotFoundError as e:
      logging.getLogger('rce_submit').critical("Job {0} not found.".
          format(e.jobid))
      print e.message()  
      return 1
    except Exception as e:
      logging.getLogger('rce_submit').critical("Unknown exception: {0}".
          format(e))
      print """
      Encountered unknown exception. Please report this to
      support@help.hmdc.harvard.edu with the following exception data:

      Exception: {0}
      """.format(e)
      return 1

  def run_app(self, application, version, memory=None, cpu=None):
    if self.rceapps.app_version_exists(application, version):
      _version = version if version else self.rceapps.get_default_version(application)
    else:
      print 'Application {0} does not exist.'
      print 'Run rce_submit.py -l to view a list of available applications.'
      return 1

    rce = HMDCCondor()

    _cpu = self.rceapps.cpu(application, _version) if cpu is None else cpu


    _memory = self.rceapps.memory(application,_version) if memory is None else memory


    job_submit_bar = ProgressBarThreadCli('* Submitting job')
    job_submit_bar.start()

    job = rce.submit(
        application,
        _version,
        self.rceapps.command(application,_version),
        self.rceapps.args(application,_version),
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

      print e.message()

      return 1
    except Exception as e:
      try:
        job_wait_bar.stop()
        job_wait_bar.join()
      except:
        pass

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

      print e.message()

      return 1
    except Exception as e:
      try:
        job_xpra_wait_bar.stop()
        job_xpra_wait_bar.join()
      except:
        pass

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

  def run(self):
    args = self.__parse_args()
    self.rceapps = rceapp.rceapp(args.config)

    
    logging.getLogger('rce_submit').setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    handler.setFormatter(logging.Formatter('%(module)s.%(funcName)s: %(message)s'))
    logging.getLogger('rce_submit').addHandler(handler)


    if args.jobs:
      self.list_jobs()
      exit(0)
    elif args.list:
      self.list_apps()
      exit(0)
    elif args.attachall:
      self.attach_all()
      exit(0)
    elif args.run and args.app:
      exit(self.run_app(args.app, args.version, args.memory, args.cpu))
    elif args.attach and isinstance(args.attach, (int, float, str)):
      self.attach_app(int(args.attach))
    else:
      exit(0)
