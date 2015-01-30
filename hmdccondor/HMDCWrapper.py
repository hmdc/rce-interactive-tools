import os
import sys
import htcondor
import classad

class HMDCWrapper:
  def __init__(self, argv):

    self.classad = classad.parseOld(
        open(os.environ['_CONDOR_JOB_AD']))

    self.cmd_orig = argv[1:]
    self.cmd = ' '.join(self.cmd_orig)

    self.app = self.classad['HMDCApplicationName']
    self.use_xpra = self.classad['HMDCUseXpra']
    self.localjobdir = self.classad['LocalJobDir'].eval()
    self.app_log = "{0}/{1}.out.txt".format(
        self.localjobdir,
        self.app)

  def __set_limits__(self):
    return 0

  def run(self):
    self.__set_limits__()
    # We need this for condor_ssh_to_job, otherwise it goes under
    # pexpect and.. bonkers!
    if self.cmd_orig[0] == '/usr/sbin/sshd':
      return self.run_sshd()
    else:
      return self.run_xpra() if self.use_xpra else self.run_screen()

  def run_sshd(self):
    os.execvpe(self.cmd_orig[0], self.cmd_orig[1:])

  def run_xpra(self):
    xpra = '/usr/bin/xpra'
    pexpect_run = '/usr/local/HMDC/bin/pexpect_run.py'
    pexpect_cmd = "{0} {1} {2}".format(pexpect_run,
        self.app_log,
        self.cmd)

    os.execlp(xpra,
        '--exit-with-children',
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


