from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import time

class RCEGraphicalTaskDispatcher(Thread):
  def __init__(self):
    super(ProgressBarThreadCli, self).__init__()
    self._stop = Event()
    return

  def stop(self):
    return self._stop.set()

  def run_one(self):
    while 1:
      time.sleep(5)
      print "1"

  def run_two(self):
    while 1:
      time.sleep(5)
      print "2"


