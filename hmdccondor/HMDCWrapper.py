import os
import sys
import htcondor
import classad
import resource
import logging
import logging.handlers

# Setup logging
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')

formatter = logging.Formatter('RceSubmit.%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

class HMDCWrapper:
  def __init__(self, argv):

    try:
      self.classad = classad.parseOld(
        open(os.environ['_CONDOR_JOB_AD']))
    except Exception as e:
      log.critical("Unable to open classad from environment variable _CONDOR_JOB_AD: {0}".format(e))
      sys.exit(1)
     
    try: 
      self.machine_ad = classad.parseOld(
        open(os.environ['_CONDOR_MACHINE_AD']))
    except Exception as e:
      log.critical("Unable to open machinead from environment variable _CONDOR_MACHINE_AD: {0}".format(e))
      sys.exit(1)

    self.cmd_orig = argv[1:]
    self.cmd = ' '.join(self.cmd_orig)

    self.app = self.classad['HMDCApplicationName']
    self.use_xpra = self.classad['HMDCUseXpra']
    self.localjobdir = self.classad['LocalJobDir'].eval()
    self.app_log = "{0}/{1}.out.txt".format(
        self.localjobdir,
        self.app)
    self.__BASENAME__ = os.path.basename(__file__)

    self.memory_bytes = (int(self.machine_ad['Memory']) * 1024) * 1024

  def __set_limits__(self):
    log.info("Setting limits on memory: {0}".format(self.memory_bytes))
    return map(lambda limit: resource.setrlimit(
      getattr(resource, limit),
      (self.memory_bytes, self.memory_bytes+1)),
      ['RLIMIT_RSS', 'RLIMIT_DATA', 'RLIMIT_AS'])

  def run(self):
    try:
      self.__set_limits__()
    except Exception as e:
      log.critical("Encountered exception setting memory limits: {0}".format(e))
      pass

    # We need this for condor_ssh_to_job, otherwise it goes under
    # pexpect and.. bonkers!
    if self.cmd_orig[0] == '/usr/sbin/sshd':
      return self.run_sshd()
    else:
      return self.run_xpra() if self.use_xpra else self.run_screen()

  def run_sshd(self):
    os.execvp(self.cmd_orig[0], 
        [self.__BASENAME__] +
        self.cmd_orig[1:])

  def run_xpra(self):
    xpra = '/usr/bin/xpra'
    pexpect_run = '/usr/bin/pexpect_run.py'
    pexpect_cmd = "{0} {1} {2}".format(pexpect_run,
        self.app_log,
        self.cmd)

    os.execlp(xpra,
        self.__BASENAME__,
        '--no-daemon',
        '--exit-with-children',
        'start',
        '--start-child={0}'.format(pexpect_cmd),
        '--socket-dir={0}'.format(os.environ['TEMP']))

    return 0

  def run_screen():
    os.environ['SCREENDIR'] = os.environ['TEMP']
    screen = '/usr/bin/screen'
    os.execvpe(screen,
        ['-L'] + self.orig_cmd,
        os.environ)


