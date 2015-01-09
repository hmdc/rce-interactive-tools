#!/usr/bin/env/python
from tabulate import tabulate
import argparse
import rceapp

def list_apps(rceapps):
  table = []
  _apps = sorted(rceapps.apps(), key=lambda s: s.lower())

  for app in _apps:
    _versions = rceapps.versions(app)
    table.append([app, _versions.pop()])
    map(lambda v: table.append(['', v]),
      _versions)

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

  args = parser.parse_args()

  _config = args.config
  _list = args.list

  rceapps = rceapp.rceapp(_config)

  # If -l, list.

  if _list:
    list_apps(rceapps)
