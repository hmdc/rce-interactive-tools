import logging

class HMDCLog:
  def __init__(self, name, level=logging.DEBUG):
    self.log = __update_settings__(logging.getLogger(name))

  def __update_handler__(self, handler):
    handler.setFormatter(logging.Formatter(
      '%(module)s.%(funcName)s: %(message)s'))
    return handler

  def __update_settings__(self, log):
    log.setLevel(level)
    log.addHandler(
      self.__update_handler__(logging.handlers.SysLogHandler(
        address='/dev/log')))
    return log
