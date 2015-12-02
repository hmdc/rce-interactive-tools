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
