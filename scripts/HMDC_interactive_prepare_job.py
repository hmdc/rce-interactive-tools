#!/usr/bin/python
import sys
import classad
import os
import pwd
# Import classad

# Debug file

f = open('/tmp/tryit.txt', 'w+')

job_classad = classad.parseOld(sys.stdin)

home = pwd.getpwnam(pwd.getpwuid(os.getuid())[0]).pw_dir
clusterid = job_classad['ClusterId']
timestamp = job_classad['LastMatchTime']
host = job_classad['RemoteHost'].split('@')[-1]

f.write(home + '\n')
f.write(str(clusterid) + '\n')
f.write(str(timestamp) + '\n')

try:
  application = job_classad['HMDCApplicationName']
  application_version = job_classad['HMDCApplicationVersion']
except:
  application = '_'.join(job_classad['OrigCmd'].split('/'))
  application_version = None

f.write(str(application) + '\n')
f.write(str(application_version) + '\n')

if application_version:
  job_dir = "{0}_{1}_{2}_{3}_{4}".format(host, clusterid, application,
      application_version, timestamp)
else:
  job_dir = "{0}_{1}_{2}_{3}".format(host, clusterid, application,
      timestamp)

f.write(str(job_dir) + '\n')

job_directory = "{0}/.HMDC/jobs/interactive/{1}".format(home, job_dir) 

os.mkdir(job_directory, 0755)

f.write(str(job_directory) + '\n')

job_classad['HMDCJobInfoDirectory'] = job_directory
job_classad['Out'] = "{0}/{1}".format(job_directory, 'out.txt')
job_classad['Err'] = "{0}/{1}".format(job_directory, 'err.txt')

sys.stdout.write (job_classad.printOld())
