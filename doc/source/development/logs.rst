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

  Unable to open machinead from environment variable _CONDOR_MACHINE_AD:
  {Exception}
  Unable to open machinead from environment variable _CONDOR_JOB_AD:
  {Exception}

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

.. note::

   See
   http://research.cs.wisc.edu/htcondor/manual/v8.4/2_5Submitting_Job.html#3382
   for more information regarding HTCondor set environment variables.

Encountered exception setting memory limits
-------------------------------------------
::
 
  Encountered exception setting memory limits: {Exception}

This is a critical error. Before a job executes, ``HMDCWrapper.py`` sets
the appropriate ulimits on the job according to to the slot's memory and
cpu allocation. While the job will still succeed in executing, this job
will not be resource limited via ulimits, just by cgroups. If you discover this
error, investigate immediately and create a ticket for RCE Development
with the full output of the log.

.. note::

   We may do away with ulimits in the future and solely rely on cgroups.
   For now, this is a critical error.


Found job in history, terminated in error
-----------------------------------------
::

  find_job_and_status(): Found job {JobId} in history. Terminated in error.

This is usually not a critical error. This means that a user submitted a
job which immediately exited. Unless the user submits a ticket, you can
safely ignore this. The following could cause this error:

* An inappropriately sized memory or cpu request.
* Application crashes -- if Matlab, XStata, or R crash upon startup for
  one reason or another, this log message will be produced.
* HTCondor misconfiguration -- unlikely, although possible.

Job took too long to start
--------------------------
::

  Oct 21 13:55:35 dev-rce6-1
  RceSubmit.esarmien.18147.HMDCLog.__rcelog_str__: run_app(): Job 148 took
  too long to start:
  Application=shell,Version=2.31.3,RequestMemory=9999,RequestCpu=9999

This is typically not a critical error and can be ignored, unless you
notice a substantial number of these messages in epylog.

The above job took too long to start because it requested 9999 GiB of
memory and 9999 CPUs. It is unlikely you'll encounter such an obvious
reason why a job took too long to start. Most often, jobs take too long
to start when:

* There are not enough resources to satisfy the job in the cluster, run
  ``rce-info.sh`` to determine the amount of resources available.

* User entered an extreme resource allocation request

* There are no execute nodes joined to the cluster (use
  ``condor_status`` to determine whether machines have joined the
  cluster) or all execute machines have ``START=FALSE``.

* Other problems in HTCondor configuration or execute nodes.


Xpra took too long to start
---------------------------
::

  run_app(): Job {jobid}, xpra took too long to start. Printing classad.

This is a critical error. When ``rce_submit.py`` submits a job, it polls
the xpra server running in the job slot on the remote execute machine to
determine whether it has started up. Upon startup, ``rce_submit.py``
launches an xpra client to connect to the launched xpra server.

If xpra took too long to start, this could mean that:

* The xpra log located in
  ``$HOME/.HMDC/interactive/{application}-{version}_{jobid}_{date}/out.txt``
  does not contain a string like ``Using display number provided by
  xpra_Xdummy: :3``. This is the string that rce_submit.py polls for to
  determine when Xpra has launched. This string could change in newer
  versions of Xpra, but, it is unlikely, and checking this is part of
  the RCE Cluster Tools development process.

* There is an XPRA error in
  ``$HOME/.HMDC/interactive/{application}-{version}_{jobid}_{date}/err.txt``. 
  Note that XPRA writes all output to stderr, so you will need to sift
  through the log and determine which errors are pertinent.

* There was an X server error. Check the appropriate ``$HOME/.xpra/Xorg.:{display}.log``

While investigating, please also create a ticket for the RCE Development
team.

Encountered unknown exception
-----------------------------

Encountered exception while removing LocalJobDir
------------------------------------------------

Error sending email notification
--------------------------------
