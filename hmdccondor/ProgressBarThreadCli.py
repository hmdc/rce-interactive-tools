from threading import Thread, Event
from time import sleep
from progressbar import ProgressBar, RotatingMarker

class ProgressBarThreadCli(Thread):
  def __init__(self, heading, maxval=140):
    # Heading can only be a str
    assert isinstance(heading, str)

    # Call Thread init
    super(ProgressBarThreadCli, self).__init__()
    self._stop = Event()
    self.maxval = maxval
    self.widgets = [ '{0}: '.format(heading),
      RotatingMarker() ]

  def stop(self):
    return self._stop.set()

  def run(self):
    pbar = ProgressBar(widgets=self.widgets, maxval=self.maxval).start()

    for i in range(self.maxval):

      if self._stop.isSet():
        break

      pbar.update(i+1)

      sleep(0.5)

    pbar.finish()
