import os
import pwd
import simpleldap
import classad
import htcondor
import hmdccondor.HMDCConstants as CONSTANTS
import hmdccondor.HMDCPoller
import re
import time
import multiprocessing as mp
import copy
import itertools
import subprocess
from datetime import datetime

def poll_thread(id,return_status,use_local_schedd):

  if use_local_schedd:
    schedd = HMDCCondor()._schedd
  else:
    schedd = htcondor.Schedd(HMDCCondor().get_sched_ad_for_job(id))

  poller = hmdccondor.HMDCPoller(id,return_status,schedd)

  return poller.run()

def poll_xpra_thread(out_txt):
  while 1:
    try:
      with open(out_txt, 'r') as out:
        line = out.readlines()
        xpra_socket = int(map(lambda _line: re.findall('Xdummy: :(\d)$', _line),line)[0][0])
        return xpra_socket
    except:
      time.sleep(5)
      continue

class HMDCCondor:
  def __init__(self):

    self._collector = htcondor.Collector(CONSTANTS.CONDOR_HOST)
    try:
      self._schedd = htcondor.Schedd()
    except:
      self._schedd = htcondor.Schedd(self._collector.locate(htcondor.DaemonTypes.Schedd))

    self._return_status = [
      CONSTANTS.JOB_STATUS_RUNNING,
      CONSTANTS.JOB_STATUS_REMOVED,
      CONSTANTS.JOB_STATUS_COMPLETED,
      CONSTANTS.JOB_STATUS_HELD,
      CONSTANTS.JOB_STATUS_SUBMIT_ERR]
    self.POLL_TIMEOUT = 90
    self.__BASENAME__ = os.path.basename(__file__)

    self.ldap_server = 'ldap.hmdc.harvard.edu'
    self.ldap_base_dn = 'dc=login,dc=hmdc,dc=harvard,dc=edu'

  def get_my_jobs(self):
    my_username = pwd.getpwuid(os.getuid())[0]

    # pwd.getpwuid() should return a string.
    assert isinstance(my_username, str)
    # it should return a username greater than 0 characters.
    assert len(my_username) > 0

    return list(itertools.chain.from_iterable(
      map(lambda schedd: htcondor.Schedd(schedd).query(
        'Owner =?= "{0}" && HMDCInteractive =?= True && HMDCUseXpra =?= True && JobStatus =?= 2'.format(my_username)), 
        self._collector.locateAll(htcondor.DaemonTypes.Schedd))))

  def get_sched_ad_for_job(self, jobid):

    try:
      ad = filter(lambda t: len(t) > 0,
          map(lambda ad: ([], ad)[len(htcondor.Schedd(ad).query(
            "ClusterId =?= {0}".format(jobid))) > 0],
            self._collector.locateAll(htcondor.DaemonTypes.Schedd)))[0]
    except:
      print "There is no HTCondor schedd currently running job\
           {0}. Perhaps your job terminated?".format(jobid)
      exit(1)

    return ad


  def get_sched_for_job(self, jobid):

    return reduce(lambda x,y: x+y,
        filter(lambda t: len(t[1]) > 0,
          map(lambda t: [t,t.query("ClusterId =?= {0}".format(jobid))],
            map(htcondor.Schedd,
              self._collector.locateAll(htcondor.DaemonTypes.Schedd)))))

  def submit(self, app_name, app_version, cmd, args, memory, cpu):

    return self._schedd.submit(self._create_classad(
      app_name,
      app_version,
      cmd,
      args,
      cpu,
      memory), 1)

  def poll(self, jobid, return_status=None,use_local_schedd=False):
    _return_status = return_status if return_status else self._return_status

    # start a thread so we can timeout on polling.
    pool = mp.Pool(1)
    result = pool.apply_async(poll_thread, (jobid, _return_status,
      use_local_schedd))
    pool.close()

    try:
      return result.get(self.POLL_TIMEOUT) 
    except:
      pool.terminate()
      raise

  def attach(self,jobid,rceapps,ad=None):

    # If attach is being run from submit, then, we don't have to poll.
    if ad is None:
      status, _classad = self.poll(jobid)
    else:
      status, _classad = classad.parseOld(ad)['JobStatus'], ad

    display = self.poll_xpra(classad.parseOld(_classad))

    return self.attach_xpra(classad.parseOld(_classad), rceapps, display)

  def attach_xpra(self, _classad, rceapps, display):
    condor_ssh = '/usr/bin/condor_ssh_to_job'
    xpra = '/usr/bin/xpra'

    job_id = int(_classad['ClusterId'])
    machine = str(_classad['RemoteHost']).split('@')[-1]
    
    return subprocess.Popen([xpra,
     "attach",
     "--socket-dir=$TEMP",
     "--tray-icon={0}".format(rceapps.icon(_classad['HMDCApplicationName'])),
     "--ssh={0} -name '{1}' {2}".format(
       condor_ssh,
       self.get_sched_ad_for_job(job_id)['ScheddIpAddr'],
       job_id),
     "ssh:{0}:{1}".format(machine, display)]).pid

  def poll_xpra(self,ad):
    _out = str(ad['Out'].eval())

    pool = mp.Pool(1)
    result = pool.apply_async(poll_xpra_thread, [_out])
    pool.close()

    try:
      return result.get(self.POLL_TIMEOUT)
    except:
      pool.terminate()
      raise

  def _create_classad(self, app_name, app_version, cmd, args, cpu, memory):
    dt = datetime.utcnow().strftime("%Y%m%d%s")

    _out = "{0}_{1}".format(app_name, app_version)

    home = pwd.getpwnam(pwd.getpwuid(os.getuid())[0]).pw_dir
    job_dir_base= "{0}/.HMDC/jobs/interactive".format(home)
    job_dir = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt)

    out = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt, '/out.txt')
    err = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt, '/err.txt')

    _classad = classad.ClassAd({
      'HMDCNewSubmit': True,
      'HMDCApplicationName': app_name,
      'HMDCApplicationVersion': app_version,
      'HMDCInteractive': True,
      'HMDCUseXpra': True,
      'JobLeaseDuration': 1200,
      'LocalJobDir': job_dir,
      'DebugPrepareJobHook': True,
      'Cmd': cmd,
      'Args': args if args else False,
      'RequestCpus': cpu,
      'RequestMemory': memory,
      'ShouldTransferFiles': 'NO',
      'TransferExecutable': False,
      'TransferIn': False,
      'Out': out,
      'Err': err,
      'Entitlements': self._get_entitlements(),
      'Environment': self._get_environment(),
      'JobNotification': 1,
      'Email': self._get_email_for_classad(),
      'FileSystemDomain': CONSTANTS.FILESYSTEM_DOMAIN
      })

    return _classad

  def _get_entitlements(self):
    # FIXME: Figure out a way to read basedn and uri from openldap
    # configuration, natively.
    _my_username = pwd.getpwuid(os.getuid())[0]

    try:
      return ' '.join(
          simpleldap.Connection(self.ldap_server, encryption='ssl')
          .search("uid={0}".format(_my_username),
            attrs = ['eduPersonEntitlement'], 
            base_dn =
            self.ldap_base_dn)[-1].values()[-1])
    except:
      # DEBUG HERE: Unable to contact LDAP server
      return classad.Value.Undefined

  def _get_email_for_classad(self):
    _email = self._get_email()
    return classad.Value.Undefined if _email is None else _email

  def _get_email(self):
    _my_username = pwd.getpwuid(os.getuid())[0]
    _email_regex = re.compile(
        "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    try:
      _emails = simpleldap.Connection(self.ldap_server, encryption='ssl').search(
          "uid={0}".format(_my_username),
          attrs = ['gecos', 'mail'],
          base_dn = self.ldap_base_dn)
    except:
      # DEBUG HERE: Unable to contact LDAP server
      return None

    assert len(_emails) == 1

    _email_from_gecos = ','.join(list(itertools.chain.from_iterable(filter(
      lambda email: len(email) > 0,
      map(
        lambda email: _email_regex.findall(email),
        _emails[0]['gecos'][0].split(','))))))

    if len(_email_from_gecos) > 0:
      return _email_from_gecos

    # Print INFO: Unable to find email

    _email_from_mail = ','.join(list(itertools.chain_from_iterable(map(
      lambda email: _email_regex.findall(email),
      _emails[0]['mail']))))

    if len(_email_from_mail) > 0:
      return _email_from_mail

    # Print unable to find any email at all
    return None





  def _get_environment(self):
    return ' '.join(filter(lambda pair: not re.match("^DBUS|^GNOME", pair), map(lambda (x,y): "%s='%s'" %(x,y), os.environ.iteritems())))
