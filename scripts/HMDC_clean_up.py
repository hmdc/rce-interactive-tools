#!/usr/bin/env python2.6
import sys
import classad
import logging
import logging.handlers
import shutil

# Setup logging
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)


def is_xpra_job(ad):
  try:
    return ad if ad['HMDCUseXpra'] else False
  except:
    log.info("Job {0} is not an xpra job. HMDCUseXpra is undefined. No clean-up required.".
        format(int(ad['ClusterId'])))
    raise

def remove_dir(dir, id):
  log.info("Removing {0} for Job {1}".format(dir, int(id)))
  return shutil.rmtree(dir)

def main():

  try:
    ad = is_xpra_job(classad.parseOne(sys.stdin.read()))
  except:
    return 0

  if ad == False:
    log.info("Job {0} has HMDCUseXpra == False. No clean-up required.".
        format(int(ad['ClusterId'])))
    return 0

  try:
    return remove_dir(ad['LocalJobDir'].eval(), ad['ClusterId'])
  except Exception as e:
    log.critical("Encountered exception while removing LocalJobDir: {0}".format(e))
    return 0


if __name__ == '__main__':
  exit(main())
