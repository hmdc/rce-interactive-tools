import logging.handlers
import logging
import pwd
import os

def rcelog(level, message, our_logger='rce_submit'):
  assert sum(map(lambda lvl: lvl == level, ['info',
    'warn', 'exception', 'error', 'debug', 'warning',
    'critical'])) > 0, "Arguments must be either \
warn, exception, error, debug, warning or critical"

  return (logging.getLogger(our_logger).__getattribute__(level))(
      message, extra={'user': pwd.getpwuid(os.getuid())[0]})
