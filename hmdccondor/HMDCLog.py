import logging

class HMDCLog:
  def __init__(self, name, level=logging.DEBUG):
    self.log = __update_settings(logging.getLogger(name))

  def __update_settings__(self, log):
    log.setLevel(level)
    log.addHandler((logging.handlers.SysLogHandler(address='/dev/log').
      setFormatter(logging.Formatter(
        '%(module)s.%(funcName)s: %(message)s'))))
    return log


