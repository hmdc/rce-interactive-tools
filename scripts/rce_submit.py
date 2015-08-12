#!/usr/bin/env/python
from tabulate import tabulate
from hmdccondor import HMDCCondor
import argparse
import rceapp

def version_string(rceapps, app, version):
  if rceapps.is_default(app,version):
    return "%s **" %(version)
  else:
    return version
    
  
def list_apps(rceapps):
  table = []
  _apps = sorted(rceapps.apps(), key=lambda s: s.lower())

  for app in _apps:
    _versions = rceapps.versions(app)
    
    table.append([app, version_string(rceapps, app, _versions.pop())])

    map(lambda v: table.append(['', version_string(rceapps, app,v)]),
        _versions)

  print "** denotes default"
  print tabulate(table, headers=["App", "Version"])

if __name__ == '__main__':

  parser = argparse.ArgumentParser(
      description = "RCE interactive job submission and access tool"
      )

  parser.add_argument('-d', '--debug', action='store_true',
      help='Enables verbose output.')

  parser.add_argument('-c', '--config',
      help='Path to rce app configuration yml (e.g.:\
      /usr/local/HMDC/etc/rceapp.yml',
      nargs='?',
      const='/etc/rceapp.yml',
      default='/etc/rceapp.yml',
      type=str,
      )

  parser.add_argument('-l', '--list', action='store_true',
      help='List supported RCE applications and versions.'
      )

  parser.add_argument('-r', '--run', action='store_true',
      help='Run a job'
      )

  parser.add_argument('-a', '--app',
      help='App to run on the RCE Cluster.'
      )

  parser.add_argument('-v', '--version', 
      help='Version of app to run on the RCE cluster'
      )

  parser.add_argument('-nogui', '--nogui', action='store_true',
      help='Set this if you want to run the app without a GUI'
      )

  parser.add_argument('-attach', '--attach',
      help='Takes a JobID as an argument. Accesses a running job.'
      )

  parser.add_argument('-jobs', '--jobs', action='store_true',
      help='Lists running jobs'
      )

  args = parser.parse_args()

  _config = args.config
  _list = args.list
  _run = args.run
  _app = args.app
  _version = args.version
  _attach = args.attach
  _list_jobs = args.jobs

  rceapps = rceapp.rceapp(_config)

  # If -l, list.

  if _list_jobs:
	print tabulate(map(lambda ad: [float(ad['ClusterId']),ad['HMDCApplicationName'],ad['HMDCApplicationVersion'],ad['RequestCpus'],ad['RequestMemory']], HMDCCondor().get_my_jobs()), headers=['Job Id', 'Application', 'Version', 'Requested Cpus', 'Requested Memory'])
	exit(0)

  if _list:
    list_apps(rceapps)
    exit(0)

  # Runtime
  
  if _attach and isinstance(_attach, (int,float,str)):
     HMDCCondor().attach(int(_attach))

  if _run and _app:
    if rceapps.app_version_exists(_app,_version):
      __version = _version if _version else rceapps.get_default_version(_app)
      hmdc_condor = HMDCCondor()
      job = hmdc_condor.submit(
          _app,
          __version,
          rceapps.command(_app,_version),
          1, 
          rceapps.memory(_app, _version),
          rceapps.args(_app,_version)
          )
      # poll for job
      job_status,classad = hmdc_condor.poll(job)
      print "Job {0} has status {1}. Attaching.".format(job, job_status)
      hmdc_condor.attach(job)
      exit(0)
    else:
      print "Application {0} does not exist.".format(_app)
      print "Run rce_submit.py -l to view a list of available applications."
      exit(1)
  elif _run:
    print "You specified -run, but did not specify an app to run.\
    Please re-run with the -a flag set to the desired application."
    exit(1)
  else:
    print "You need to specify either -r, or -l."
    exit(1)

