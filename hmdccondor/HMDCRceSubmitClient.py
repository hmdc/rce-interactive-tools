from tabulate import tabulate
from hmdccondor import HMDCCondor
from hmdccondor import RCEJobNotFoundError, \
  RCEJobTookTooLongStartError, \
  RCEXpraTookTooLongStartError, \
  RCEJobDidNotStart, \
  RCEConsoleClient, \
  RceSubmitLaunch, \
  rcelog
from ProgressBarThreadCli import ProgressBarThreadCli
import argparse
import rceapp
import logging
import logging.handlers
import wx

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

    parser.add_argument('-graphical', '--graphical',
        action='store_true',
        help='Use rce_submit gui',
        default=False,
        )

    parser.add_argument('-nogui', '--nogui', action='store_true',
        help='Set this if you want to run the app without a GUI',
        default=False,
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

  def attach_all(self, rceapps):
    return RCEConsoleClient(rceapps).attach_all()

  def attach_app(self, rceapps, jobid):
    return RCEConsoleClient(rceapps).attach_app(jobid)

  def run_app(self, rceapps, application, version, memory, cpu, graphical):

    def gb_to_mb(n):
      return n*1024 if isinstance(n, int) else n

    return RCEConsoleClient(rceapps, application, version,
        gb_to_mb(memory), cpu).run_app() if graphical is False else RceSubmitLaunch(0,
 		rceapps = rceapps,
		application = application,
		version = version,
		memory = gb_to_mb(memory),
		cpu = cpu)()

  def list_jobs(self):
    print self.__list_jobs()

  def list_apps(self):
    print "** denotes default"
    print self.__list_apps()

  def run(self):
    args = self.__parse_args()
    self.rceapps = rceapp.rceapp(args.config)
 
    logging.getLogger('rce_submit').setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    handler.setFormatter(logging.Formatter('RceSubmit.%(user)s.%(process)d.%(module)s.%(funcName)s: %(message)s'))
    logging.getLogger('rce_submit').addHandler(handler)


    if args.nogui:
      print """\
--nogui is currently unimplemented. Future versions will allow users to submit
non-graphical interactive jobs.\
"""
      exit(0)
    elif args.jobs:
      self.list_jobs()
      exit(0)
    elif args.list:
      self.list_apps()
      exit(0)
    elif args.attachall:
      self.attach_all(self.rceapps)
      exit(0)
    elif args.run and args.app:
      exit(self.run_app(self.rceapps, args.app, args.version, args.memory, args.cpu,
        args.graphical))
    elif args.attach and isinstance(args.attach, (int, float, str)):
      self.attach_app(self.rceapps, int(args.attach))
    else:
      exit(0)
