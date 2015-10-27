from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from wx import CallAfter
from HMDCCondor import HMDCCondor
from threading import Thread, Event

class RCEGraphicalTaskDispatcher(Thread):
  def __init__(self, f, *args):
    super(RCEGraphicalTaskDispatcher, self).__init__()
    self._stop = Event()
    self.rce = HMDCCondor()
    self.f = getattr(self, f)
    self.args = args
    return

  def stop(self):
    return self._stop.set()

  def run(self):
    self.f(*self.args)

  def run_app(self, application, version, command, args, memory, cpu):
    job = self.rce.submit(application, version, command, args, memory, cpu)
    CallAfter(pub.sendMessage, 'rce_submit.job_submitted',
        jobid = job)

  def poll_app(self, jobid):
    try:
      job_status, ad = self.rce.poll(jobid, use_local_schedd=True)
      CallAfter(pub.sendMessage, 'rce_submit.job_started',
         job_status=job_status, ad=ad, excpt=None)
    except Exception as e:
      CallAfter(pub.sendMessage, 'rce_submit.job_started', job_status=None,
        ad=None, excpt=e)

  def attach_app(self, rceapps, jobid, ad):
    try:
      CallAfter(pub.sendMessage, 'rce_submit.xpra_attached',
          pid = self.rce.attach(jobid, rceapps, ad=ad),
          excpt = None)
    except Exception as e:
      CallAfter(pub.sendMessage, 'rce_submit.xpra_attached',
          pid = None,
          excpt = e)
