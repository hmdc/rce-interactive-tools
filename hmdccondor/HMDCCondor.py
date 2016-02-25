"""
HMDCCondor module provides most-commonly-used functions for interacting with
HTCondor clusters: polling for job status, acquiring schedd objects, and
submitting jobs according to the HMDC ClassAd schema. This replaces
Condor.pm in the hmdc-admin repository.
"""

__author__ = "Evan Sarmiento"
__email__ = "esarmien@g.harvard.edu"

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
import logging
from datetime import datetime
from hmdccondor import RCEJobNotFoundError, \
    RCEJobTookTooLongStartError, \
    RCEXpraTookTooLongStartError, \
    RCEJobDidNotStart
from hmdccondor.HMDCLog import rcelog

def poll_thread(id,return_status,use_local_schedd):
  """poll_thread is a function which when provided as an argument to
     `apply_async()
     <https://docs.python.org/2/library/multiprocessing.html>`_
     is executed in an independent thread.
     ``poll_thread`` creates a new ``HMDCPoller`` which runs until the
     job represented by ``id`` has a ``JobStatus`` equal to any number in
     the ``return_status`` array.

     :param id: HTCondor Job Id to poll for
     :type id: ``int``
     :param return_status: An array of JobStatus values to look for.
     :type return_status: ``list``
     :param use_local_schedd: If set to true, uses the schedd of the executing host. If false, finds the schedd whcih submitted the HTCondor job represented by **id**.
     :type use_local_schedd: ``boolean``
     :returns: ``(JobStatus, ClassAd)`` or ``(None,None)`` if no such job exists.
     :rtype: ``tuple``

     :Example:

     >>> import hmdccondor
     >>> from hmdccondor.HMDCCondor import poll_thread
     >>> poll_thread(10, [1,2,3,4,5], True)

  """

  if use_local_schedd:
    return hmdccondor.HMDCPoller(id, return_status, HMDCCondor()._schedd).run()
  else:
    try:
      return hmdccondor.HMDCPoller(id, return_status, htcondor.Schedd(HMDCCondor().get_sched_ad_for_job(id))).run()
    except:
      return (None,None)

def poll_xpra_thread(out_txt):
  """``poll_xpra_thread`` is a function when provided as an argument to
     `apply_async()
     <https://docs.python.org/2/library/multiprocessing.html>`_
     is executed in an independent thread. ``poll_xpra_thread`` continues to read
     ``out_txt``, which is the location of the Xpra startup log file, to determine
     if xpra has started within a job.

     :param out_txt: Fully qualified path of Xpra startup log file
     :type out_txt: ``str``
     :returns: Xpra display number
     :rtype: ``int``

     :Example:

     >>> from hmdccondor import poll_xpra_thread
     >>> poll_xpra_thread('/nfs/home/E/esarmien/.HMDC/jobs/interactive/xstata-mp_14.0_174_201510271445990519/out.txt')

  """

  while 1:
    try:
      with open(out_txt, 'r') as out:
        return int(map(lambda _line: re.findall('Xdummy: :(\d+)$',
          _line),out.readlines())[0][0])
    except:
      time.sleep(5)
      continue

class HMDCCondor:
  """HMDCCondor provides an interface to a local HTCondor cluster. It
  instantiates a local HTCondor schedd object for all operations. The
  initialization method for the HMDCCondor class acquires a local
  HTCondor schedd object, sets the polling timeout, and local LDAP
  server.

  .. note::

    self.ldap_server and self.ldap_base_dn should be acquired via
    rceapp.yml rather than statically defined in __init__()

  """

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
    """``get_my_jobs()`` returns an array of jobs your username is currently
    running and has a ``JobStatus =?= 2``.

    :returns: list of jobs you're running
    :rtype: ``list``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor().get_my_jobs()

    """
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
    """get_sched_ad_for_job() returns the classad for the schedd
    currently running a job with id ``jobid``

    :param jobid: job id
    :type jobid: ``int``
    :returns: classad of schedd
    :rtype: ``classad.ClassAd``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor().get_sched_ad_for_job(73)

    """

    try:
      return filter(lambda t: len(t) > 0,
          map(lambda ad: ([], ad)[len(htcondor.Schedd(ad).query(
            "ClusterId =?= {0}".format(jobid))) > 0],
            self._collector.locateAll(htcondor.DaemonTypes.Schedd)))[0]
    except:
      raise

  def get_sched_for_job(self, jobid):
    """get_sched_for_job() returns an htcondor.Schedd object for the
    schedd currently running a job with id ``jobid``

    :param jobid: job id
    :type jobid: ``int``
    :returns: htcondor Schedd object
    :rtype: ``htcondor.Schedd``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor().get_sched_for_job(73)

    """

    return reduce(lambda x,y: x+y,
        filter(lambda t: len(t[1]) > 0,
          map(lambda t: [t,t.query("ClusterId =?= {0}".format(jobid))],
            map(htcondor.Schedd,
              self._collector.locateAll(htcondor.DaemonTypes.Schedd)))))

  def submit(self, app_name, app_version, cmd, args, memory, cpu):
    """submit() submits a job to the HTCondor cluster using the
    specified arguments.

    :param app_name: application name
    :type app_name: ``str``
    :param app_version: application version
    :type app_version: ``str``
    :param cmd: command to run on htcondor cluster
    :type cmd: ``str``
    :param args: arguments to command
    :type args: ``list``
    :param memory: amount of memory required for job
    :type memory: ``int``
    :param cpu: amount of cpus required for job
    :type cpu: ``int``
    :returns: jobid of submitted job
    :rtype: ``int``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor().submit('Shell, '2.31.3', '/usr/bin/gnome-terminal',
        [], 2048, 1)

  """

    return self._schedd.submit(self._create_classad(
      app_name,
      app_version,
      cmd,
      args,
      cpu,
      memory), 1)

  def poll(self, jobid, return_status=None, use_local_schedd=False, want_results=[CONSTANTS.JOB_STATUS_RUNNING]):
    """poll() takes a job id and returns a ``(JobStatus,ClassAd)`` tuple if,
    before the polling timeout window exceeds, a job has a ``JobStatus``
    classad element which matches an integer in the ``return_status`` array.
    It then compares this ``JobStatus`` to the ``want_results`` array. If the
    job polled has a ``JobStatus`` which is also in the ``want_results`` array,
    poll succeeds, otherwise, raises an exception.

    :param jobid: job id
    :type jobid: ``int``
    :param return_status: an array of JobStatus's from which polling
      should return.
    :type return_status: ``list``
    :param use_local_schedd: If true, uses local schedd, otherwise finds
      schedd for jobid.
    :type use_local_schedd: ``bool``
    :param want_results: An array of JobStatus values that are compared
      to the JobStatus of the successfully returned job.
    :type want_results: ``list``
    :returns: ``(JobStatus, ClassAd)`` of polled job
    :rtype: ``tuple``
    :raises:
      :py:exc:`hmdccondor.HMDCExceptions.RCEJobDidNotStart`
    :raises:
      :py:exc:`hmdccondor.HMDCExceptions.RCEJobTookTooLongStartError`

    :Example:

    >>> from hmdccondor import HMDCCondor, CONSTANTS
    >>> HMDCCondor().poll(73, return_status=[2], use_local_schedd=True,
      want_results = [ CONSTANTS.JOB_STATUS_RUNNING ])

    """

    assert isinstance(want_results, list)
    assert isinstance(use_local_schedd, bool)

    def check_result(result):
      if result[0] in want_results:
        return result
      else:
        raise RCEJobDidNotStart(result)

    _return_status = return_status if return_status else self._return_status

    # start a thread so we can timeout on polling.
    pool = mp.Pool(1)
    result = pool.apply_async(poll_thread, (jobid, _return_status,
      use_local_schedd))
    pool.close()

    try:
      return check_result(result.get(self.POLL_TIMEOUT))
    except RCEJobDidNotStart:
      pool.terminate()
      raise
    except Exception as e:
      pool.terminate()
      raise RCEJobTookTooLongStartError(jobid)

  def attach(self,jobid,rceapps,ad=None):
    """
    attach() executes the xpra client to connect to an xpra server
    running as job ``jobid`` on the htcondor cluster.

    :param jobid: job id
    :type jobid: ``int``
    :param rceapps: rceapps object
    :type rceapps: rceapp.rceapp
    :param ad: ClassAd for job, specified by jobid. If present, attach()
      does not poll for job classad, since it's provided. This ClassAd
      should be unformatted str.
    :type ad: ``str``
    :returns: pid of executed xpra client
    :rtype: ``int``
    :raises:
      :py:exc:`hmdccondor.HMDCExceptions.RCEJobNotFoundError`

    :Example:

    >>> from rceapp import rceapp
    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor().attach(75, rceapp('/etc/rceapp.yml'))

    """
    # If attach is being run from submit, then, we don't have to poll.

    if ad is None:
      status, _classad = self.poll(jobid, want_results= [None, CONSTANTS.JOB_STATUS_RUNNING] )
    else:
      status, _classad = classad.parseOne(ad)['JobStatus'], ad

    if status is None or _classad is None:
      raise RCEJobNotFoundError(jobid)

    return (lambda ad: self.attach_xpra(ad, rceapps,
      self.poll_xpra(ad)))(classad.parseOne(_classad))

  def attach_xpra(self, _classad, rceapps, display):
    """
    attach_xpra() executes the xpra client to connect to an xpra server
    running under the job specified by _classad on the display specified
    by **display**. This should probably not be used on its own, and
    instead, the higher order function attach() should be called.

    :param _classad: classad for job
    :type _classad: ``classad.ClassAd``
    :param rceapps: rceapps object
    :type rceapps: rceapp.rceapp
    :param display: display id for xpra server
    :type display: ``int``
    :returns: pid of executed xpra client
    :rtype: ``int``

    :Example:

    >>> from rceapp import rceapp
    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor().attach_xpra((HMDCCondor().poll(75))[1],
      rceapp('/etc/rceapp.yml'), 3)

    """

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
     "ssh:{0}:{1}".format('', display)], env=dict(os.environ, SSH_AUTH_SOCK="")).pid

  def poll_xpra(self,ad):
    """poll_xpra() creates a thread which polls the xpra server log to
    determine if the xpra server has been started.

    :param ad: classad of the xpra-enabled job to poll
    :type ad: ``classad.ClassAd``
    :returns: display number of xpra server
    :rtype: ``int``
    :raises:
      :py:exc:`hmdccondor.HMDCExceptions.RCEXpraTookTooLongStartError`

    """
    _out = str(ad['Out'].eval())

    pool = mp.Pool(1)
    result = pool.apply_async(poll_xpra_thread, [_out])
    pool.close()

    try:
      return result.get(self.POLL_TIMEOUT)
    except:
      pool.terminate()
      raise RCEXpraTookTooLongStartError(ad)

  def _create_classad(self, app_name, app_version, cmd, args, cpu, memory):
    """_create_classad() creates a classad for submission to the
    htcondor cluster, utilizing HMDC custom ClassAds.

    :param app_name: application name
    :type app_name: ``str``
    :param app_version: application version
    :type app_version: ``str``
    :param cmd: command to run
    :type cmd: ``str``
    :param args: args to pass to cmd
    :type args: ``list``
    :param memory: memory to reserve for job
    :type memory: ``int``
    :returns: classad object
    :rtype: ``classad.ClassAd``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor()._create_classad('shell', '2.1.32',
      '/usr/bin/gnome-terminal', [], 1, 2048)

    """
    dt = datetime.utcnow().strftime("%Y%m%d%s")

    _out = "{0}_{1}".format(app_name, app_version)

    home = pwd.getpwnam(pwd.getpwuid(os.getuid())[0]).pw_dir
    job_dir_base= "{0}/.HMDC/jobs/interactive".format(home)
    job_dir = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt)

    out = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt, '/out.txt')
    err = classad.Function('strcat', job_dir_base, '/', _out, '_', classad.ExprTree('ClusterId'), '_', dt, '/err.txt')

    _email = self._get_email_for_classad()

    _classad = classad.ClassAd({
      'AcctGroup': 'group_interactive',
      'AcctGroupUser': pwd.getpwuid(os.getuid())[0],
      'AccountingGroup': "group_interactive.{0}".format(pwd.getpwuid(os.getuid())[0]),
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
      'NotifyUser': _email,
      'Email': _email,
      'FileSystemDomain': CONSTANTS.FILESYSTEM_DOMAIN
      })

    rcelog('info', "Generated classad for submission. ClassAd printed below.")
    rcelog('info', _classad)

    return _classad

  def _get_entitlements(self):
    """_get_entitlements() returns a space-separated list of ldap
    entitlements.

    :returns: space-separated list of ldap entitlements, or
      ``classad.Value.Undefined`` if ldap server is unreachable
    :rtype: ``str``
    :rtype: ``classad.Value.Undefined``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor()._get_entitlements()

    """
    # FIXME: Figure out a way to read basedn and uri from openldap
    # configuration, natively.
    _my_username = pwd.getpwuid(os.getuid())[0]

    try:
      return ','.join(
          simpleldap.Connection(self.ldap_server, encryption='ssl')
          .search("uid={0}".format(_my_username),
            attrs = ['eduPersonEntitlement'], 
            base_dn =
            self.ldap_base_dn)[-1].values()[-1])
    except:
      # DEBUG HERE: Unable to contact LDAP server
      rcelog('critical', "_get_entitlements(): Unable to contact ldap server {0}".format(self.ldap_server))
      return classad.Value.Undefined

  def _get_email_for_classad(self):
    """_get_email_for_classad() is used to set the Email field in a
    classad. This wraps _get_email(). If _get_email() cannot find an
    email address in the users' ldap field, it returns
    classad.Value.Undefined.

    :returns: e-mail address or classad.Value.Undefined
    :rtype: ``str``
    :rtype: ``classad.Value.Undefined``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor()._get_email_for_classad()

    """
    return (lambda email: classad.Value.Undefined if email is None else email)(self._get_email())

  def _get_email(self):
    """get_email() attempts to find users' email in gecos field or mail
    ldap field. If unable to find in either, returns None.

    :returns: e-mail address or None
    :rtype: ``str``
    :rtype: ``None``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor()._get_email()

    """
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
      rcelog('critical', "_get_email(): Unable to contact ldap server {0}".format(self.ldap_server))
      return None

    assert len(_emails) == 1

    _email_from_gecos = ','.join(list(itertools.chain.from_iterable(filter(
      lambda email: len(email) > 0,
      map(
        lambda email: _email_regex.findall(email),
        _emails[0]['gecos'][0].split(','))))))

    if len(_email_from_gecos) > 0:
      rcelog('info', "_get_email(): Found email {0} in gecos field.".format(_email_from_gecos))
      return _email_from_gecos

    # Print INFO: Unable to find email

    rcelog('critical', "_get_email(): Unable to find email in gecos field. Using mail field.")

    _email_from_mail = ','.join(list(itertools.chain_from_iterable(map(
      lambda email: _email_regex.findall(email),
      _emails[0]['mail']))))

    if len(_email_from_mail) > 0:
      rcelog('info', "_get_email(): Found email in mail field: {0}".format(_email_from_mail))
      return _email_from_mail

    # Print unable to find any email at all
    rcelog('critical', "_get_email(): Unable to find email in either gecos or mail field. Investigate.")
    return None

  def _get_environment(self):
    """_get_environment() returns a space-separated list of user
    environment variables as key,value pairs for use in a classad.

    :returns: string of environment variables, values separated by
      spaces
    :rtype: ``str``

    :Example:

    >>> from hmdccondor import HMDCCondor
    >>> HMDCCondor()._get_environment

    """

    return ' '.join(filter(lambda pair: not re.match("^DBUS|^GNOME", pair), map(lambda (x,y): "%s='%s'" %(x,y), os.environ.iteritems())))
