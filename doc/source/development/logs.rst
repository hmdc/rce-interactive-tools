Epylog messages
===============

.idletime
------------------------
::

  Nov 30 11:09:03 exec6-3 HMDC_periodic_job_is_idle.get_current_idle_time:
  Job 33727.0: Unable to read .idletime file: [Errno 2] No such file or
  directory: '/tmp/condor/execute/dir_85231/.idletime'

  Nov 30 11:09:03 exec6-3 HMDC_periodic_job_is_idle.get_last_check_time:
  Job 33727.0: Failure reading last_check_time from#012.idletime file,
  exception: [Errno 2] No such file or directory:
  '/tmp/condor/execute/dir_85231/.idletime'

``HMDC_periodic_job_is_idle.py`` is run periodically for every job
currently executing. It calculates idletime by determing whether the
currently executing job is idle, and, if it is, incrementing the job's
idletime found in ``$TEMP/.idletime``. ``$TEMP`` references the job's
execute directory under ``/tmp/condor/execute``.

If ``$TEMP/.idletime`` does not exist, ``HMDC_periodic_job_is_idle.py`` will
write this error to syslog, but then create ``$TEMP/.idletime`` with a
value of 0. ``$TEMP/.idletime`` does not exist when a job begins to
execute, so this error is expected and can be ignored.

However, if the logged exception is something other than ``No such file
or directory``, Operations should create a new ticket for the RCE
Development team.

.. note::

   ``HMDC_job_wrapper.py`` should create a blank ``$TEMP/.idletime`` upon
   job execution such that these errors aren't logged unnecessarily.

Unable to find email in either gecos or mail field
--------------------------------------------------
::

  RceSubmit.esarmien.31662.HMDCLog.__rcelog_str__: _get_email(): Unable
  to find email in either gecos or mail field. Investigate


``rce_submit.py`` sets the ``Email`` field of the submitted ClassAd by
looking for the user's email address first in the ``gecos`` field, then
in the ``mail`` field. If an email address is found in neither,
Operations should investigate in order to fix the erroneous LDAP record.
If the LDAP record is found not to be erroneous, open a ticket with the
RCE Development Team.

Unable to open job classad or machinead
---------------------------------------
::

  Unable to open machinead from environment variable _CONDOR_MACHINE_AD
  Unable to open machinead from environment variable _CONDOR_JOB_AD

``HMDCWrapper.py`` opens the job classad and machine classads referenced
by environment variables set by HTCondor ``_CONDOR_MACHINE_AD`` and
``_CONDOR_JOB_AD``. When a job executes, HTCondor writes the machinead
and the job classad to the job's execute directory in ``/tmp/condor/execute`` as
``.machine.ad`` and ``.job.ad`` respectively.

This is a critical error and you should never see this. If this error
does occur, it could mean that free space on ``/tmp``, the parent
directory of all HTCondor execute directories, is exhausted and HTCondor
is unable to write these files. If you discover that ``/tmp`` is indeed
full, clear out the problematic files and ask the impacted users to
resubmit their jobs.

If ``/tmp`` is not full, this error indicates a more serious problem.
Investigate and create a ticket in the RCE Development queue.

Encountered exception setting memory limits
-------------------------------------------

Found job in history, terminated in error
-----------------------------------------

Xpra took too long to start
---------------------------

Encountered unknown exception
-----------------------------

Encountered exception while removing LocalJobDir
------------------------------------------------

Error sending email notification
--------------------------------
