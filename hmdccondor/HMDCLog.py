import logging.handlers
import logging
import pwd
import os
import classad

def rcelog(level, message, our_logger='rce_submit',
    my_username=pwd.getpwuid(os.getuid())[0]):

  def __rcelog__():
    return getattr(logging.getLogger(our_logger), level)

  def __rcelog_str__():
    return (__rcelog__())(message, extra={'user': my_username})

  def __rcelog_ad__():
    return map(lambda adpair: (__rcelog__())("{0}={1}".format(adpair[0], adpair[1]),
      extra={'user': my_username}), message.items())

  assert isinstance(message, str) or isinstance(message, classad.ClassAd)
  assert sum(map(lambda lvl: lvl == level, ['info',
    'warn', 'exception', 'error', 'debug', 'warning',
    'critical'])) > 0, "Arguments must be either \
warn, exception, error, debug, warning or critical"

  return __rcelog_ad__() if isinstance(message, classad.ClassAd) else __rcelog_str__()
