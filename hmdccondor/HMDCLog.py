"""
Provides a series of functions which wrap logging functionality.
"""

import logging.handlers
import logging
import pwd
import os
import classad

def exception_helper(excpt):
  """a wrapper for an HMDC defined exception. All HMDC defined
  exceptions in this project contain the message() class method, whereas
  all other exceptions do not. Passing an exception to this function
  will either return the value of the message() class method or return a
  string which says that that the application has encountered an unknown
  exception and to contact support.

  :param excpt: exception
  :type excpt: Exception
  :returns: explanatory text wrt. exception
  :rtype: str

  """
  try:
    return excpt.message()
  except:
    return """
Encountered unknown exception. Please report
this to support@help.hmdc.harvard.edu with
the following exception data:

Exception: {0}.format(excpt)
"""

def rcelog(level, message, our_logger='rce_submit',
    my_username=pwd.getpwuid(os.getuid())[0]):
  """this function wraps the logger class methods. Its primary feature
  is to add the username of the executing user to the syslog message for
  debugging purpose.

  :param level: debugging level for log message
  :type level: str
  :param message: message to log
  :type message: str
  :param our_logger: name of logger
  :type our_logger: str
  :param my_username: username to append to log message, defaults to
    executing user.
  :type my_username: str

  """

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
