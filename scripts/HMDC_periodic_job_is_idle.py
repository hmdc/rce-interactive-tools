#!/usr/bin/env python2.6
import sys
import classad
import htcondor
import logging
import logging.handlers
import os
import smtplib
import re
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from hmdccondor import HMDCCondor
# Import classad

# Setup logging
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

def check_if_preempt(ad,
    idletime,
    notice_lock_file = "{0}/.sent-notice".format(
      os.environ['TEMP'])):

  def __when_preemptible__():
    try:
      return int(classad.ExprTree(
        htcondor.param.get('IDLE_WARNING_TRIGGER')).eval())
    except Exception as e:
      log.critical("""Could not find or evaluate IDLE_WARNING_TRIGGER in
      HTCondor configuration. Returning None. Exception:
      {0}""".format(e))
      return None

  def __notice_lock_file_exists__():
    return os.path.isfile(notice_lock_file)

  def __log_is_not_preempt__(f):
    log.info("Job {0} is not preemptible. ! {1} > {2}.".format(
      int(ad['ClusterId']),
      idletime,
      __when_preemptible__()))

    return f

  def __remove_notice_lock_file__(exists = __notice_lock_file_exists__()):
    try:
      return os.remove(notice_lock_file) if exists else 0
    except Exception as e:
      log.critical("Error removing lockfile {0}, exception: {1}".format(
        notice_lock_file, e))
      raise

  def __create_notice_lock_file__():
    try:
      return os.mknod(notice_lock_file)
    except Exception as e:
      log.critical("Error creating lockfile {0}, exception: {1}".format(
        notice_lock_file, e))
      raise

  def __can_be_preempt__(time_to_preempt):
    return __do_notice__() if idletime >= \
        time_to_preempt and __is_an_xpra_job__() else \
        __log_is_not_preempt__(__remove_notice_lock_file__())

  def __sanitize_email__(mail,
      mail_regex=re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")):

    if mail_regex.match(mail):
      return mail
    else:
      log.critical("Email address {0} in ClassAd is not a valid email address.".format(mail))
      raise Exception("Email address {0} invalid.".format(mail))

  def __send_notice__():
    try:
      notice = MIMEMultipart()

      notice['Subject'] = 'Warning: Job {0}: {1} {2} has been idle for {3} days'.format(
        int(ad['ClusterId']),
        ad['HMDCApplicationName'],
        ad['HMDCApplicationVersion'],
        idletime // 86400)


      notice.attach(MIMEText(
"""
Dear {0},

Your RCE powered job {1} {2} has been idle for {3} days. If your job
remains idle for three or more days, your job will become preemptible.

Under conditions of RCE cluster saturation, RCE powered jobs, idle for
three or more days, can be pre-empted in order to satisfy resource
requirements of newly submitted RCE powered jobs. If your RCE powered
job is pre-empted, you will lose all currently unsaved work within that
job. If you don't plan on actively utilizing {1} {2} within the next
day, please make sure to save your work or terminate your job if you've
successfully accomplished your tasks. Otherwise, using {1} within the
next 24 hours will stave off pre-emptability for another two days.

If you believe you've received this message in error, please e-mail
rce_services@help.hmdc.harvard.edu.

Best,
RCE Development and Support Team
""".format(ad['Owner'], ad['HMDCApplicationName'],
           ad['HMDCApplicationVersion'], idletime / 86400)))

      notice['From'] = 'rce_services@help.hmdc.harvard.edu'
      try:
        notice['To'] = __sanitize_email__(ad['Email'])
      except:
        log.critical('No Email field defined in ClassAd for Job {0}. Look into this immediately.'.
          format(ad['ClusterId']))
        raise

      log.info('Sending e-mail notice to {0}'.format(ad['Email']))

      # Un-necessary logging, but you can uncomment this if you want to
      # see the actual email in syslog
      # print notice.as_string()

      s = smtplib.SMTP('localhost')
      s.sendmail(
          notice['From'],
          [notice['To']],
          notice.as_string())
      s.quit()

      log.info('Email successfully sent to {0}'.format(ad['Email']))

      return __create_notice_lock_file__()
    except Exception as e:
      log.critical('Error sending email notification: {0}'.format(e))
      log.critical('Setting job {0} IdleTime to 0 due to exception'.format(
        ad['ClusterId']))

      update_job("{0}.{1}".format(
        str(ad['ClusterId']),
        str(ad['ProcId'])),
        False,
        ad)

      return 1 if not __notice_lock_file_exists__() else __remove_notice_lock_file__()

  def __is_an_xpra_job__():
    try:
      return ad['HMDCUseXpra']
    except:
      return False

  def __do_notice__():
    log.info("Job {0} can be preempted: Job[{0}][JobCpuIdleTime] > {1}".
        format(int(ad['ClusterId']), __when_preemptible__()))

    if __notice_lock_file_exists__():
      log.info("""For Job {0}, User {1} has already been notified of
      impending preemptibility""".format(int(ad['ClusterId']),
        ad['Owner']))
      return 0

    return __send_notice__()

  return 0 if __when_preemptible__() is None else __can_be_preempt__(
      __when_preemptible__())

def update_job(jobid, is_job_idle, q_classad):

  def get_last_check_time():
    try:
      return int(os.path.getmtime('{0}/.idletime'.format(os.environ['TEMP'])))
    except Exception as e:
      log.critical("""Job {0}: Failure reading last_check_time from
.idletime file, exception: {1}""".format(jobid, e))
      return 0

  def get_current_time():
    return int(q_classad['CurrentTime'].eval())

  def get_current_idle_time():
    try:
      with open('{0}/.idletime'.format(os.environ['TEMP']), 'r') as itf:
        return int(itf.readline().strip())
    except Exception as e:
      log.critical('Job {0}: Unable to read .idletime file: {1}'.format(
        jobid, e))
      return 0

  def evaluate_new_idle_time(ct=get_current_time()):

    def __evaluate_new_idle_time__(ct):
      return (ct, get_current_idle_time() + (ct -
        (get_last_check_time() or ct)))

    try:
      return ((is_job_idle and __evaluate_new_idle_time__(ct)) or (ct,
        0))
    except:
      return (ct, 0)

  def set_idle_time(current_time, idle_time):

    log.info('Job {0}: LastIdleCheckTime={1}, JobCpuIdleTime={2}'.format(
      jobid,
      current_time,
      idle_time))
    try:
      with open("{0}/.idletime".format(os.environ['TEMP']), 'w') as f:
        f.write(str(idle_time))
    except Exception as e:
      log.critical('Job {0}: Unable to open .idletime file in TEMP: {1}'.
          format(jobid, e))
      return 0

    return idle_time


  return set_idle_time(*evaluate_new_idle_time())


def main(job_classad = classad.parseOld(sys.stdin)):

  jobid = lambda ad: "{0}.{1}".format(
      str(ad['ClusterId']),
      str(ad['ProcId']))

  is_interactive = lambda ad: job_classad['HMDCInteractive']

  try:
    if not is_interactive(job_classad):
      return 0
  except:
    return 0

  # If the job isn't currently running, we don't care.
  if 2 > job_classad['JobStatus'] > 2:
    log.info('Job is no longer running, exiting.')
    return 0

  log.info ('Job {0}: Running.'.format(jobid(job_classad)))

  try:
    is_job_idle = HMDCCondor()._collector.query(htcondor.AdTypes.Any,
        'JobId =?= "{0}"'.format(jobid(job_classad)),
        ['JobCpuIsIdle'])[0]['JobCpuIsIdle'].eval()
    log.info('Job {0}: Idle? {1}'.format(jobid(job_classad), is_job_idle))
  except:
    log.info('Job {0}: Unable to evaluate JobCpuIsIdle'.format(jobid(job_classad)))
    return 0

  return check_if_preempt(job_classad, update_job(jobid(job_classad),
    is_job_idle, job_classad))

if __name__ == '__main__':
  exit(main())
