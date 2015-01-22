#!/usr/bin/env/python
from tabulate import tabulate
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
      required=True
      )
  parser.add_argument('-l', '--list', action='store_true',
      help='List supported RCE applications and versions.'
      )

  parser.add_argument('-r', '--run', action='store_true',
      help='Run a job'
      )

  parser.add_argument('-a', '--app', action='store_true',
      help='App to run on the RCE Cluster.'
      )

  parser.add_argument('-v', '--version', action='store_true',
      help='Version of app to run on the RCE cluster'
      )

  parser.add_argument('-nogui', '--nogui', action='store_true',
      help='Set this if you want to run the app without a GUI'
      )

  parser.add_argument('-attach', '--attach', action='store_true',
      help='Takes a JobID as an argument. Accesses a running job.'
      )

  parser.add_argument('-list-jobs', '--list-jobs', action='store_true',
      help='Lists running jobs'
      )

  args = parser.parse_args()

  _config = args.config
  _list = args.list

  rceapps = rceapp.rceapp(_config)

  # If -l, list.

  if _list:
    list_apps(rceapps)
    exit(0)
