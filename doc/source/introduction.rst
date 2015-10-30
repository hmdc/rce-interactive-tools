:orphan:

RCE Cluster Tools
=================

The Research Computing Environment (RCE) cluster tools package,
installed on every RCE login node accessible via NoMachine NX4, allows
you to submit interactive jobs to HMDC's local HTCondor pool.

RCE cluster tools replaces **condorInteractiveSubmit**, an
interactive job submission utility executed whenever you ran an RCE
Powered job.

While RCE cluster tools is new, the user interface is not substantially
different from **condorInteractiveSubmit**. You can submit RCE powered jobs exactly as
you have before. However, under the hood, RCE cluster tools allows you
to:

* **Submit persistent interactive jobs**: Even when the RCE login nodes are
  rebooted or undergo maintenance, interactive jobs submitted via RCE
  cluster tools will continue to run and can be re-attached to any RCE
  desktop.

* **Forget about renewing job leases**: You can now run RCE powered
  applications for as long as you want without requesting extensions, 
  provided your job does not remain idle for more than two days.

This manual will teach you how to perform the following tasks:

* Submit an RCE interactive job
* Re-attach an RCE interactive job
* Understand idle-time based job management

For a more general overview of the technology behind RCE cluster tools,
read `*Always On: Persistent Interactive Jobs on the RCE* <http://projects.iq.harvard.edu/rce/blog/always-persistent-interactive-jobs-rce>`_
