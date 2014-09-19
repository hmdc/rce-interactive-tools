rce-interactive-tools
=====================

How to Run the SysTray Example
==============================
* This example is a simple systray applet.
* When you Right-Click on it, the applet displays the Job-ID and the
  RemoteMachine your job is running on
* When you click the Job, the systray applet exists.

Pre-Req
=======
* Only works in Python 2.6 (Condor module only works in 2.6)
* Runs on dev-rce6-1/2.hmdc.harvard.edu
```shell
sudo yum -y install wxpython
cd ./condor_sys_tray_example
python htcondor_job_systray.py
```

