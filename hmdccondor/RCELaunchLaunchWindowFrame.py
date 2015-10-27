# -*- coding: UTF-8 -*-
#
# generated by wxGlade not found on Sun Oct 25 22:13:19 2015
#
import time
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import classad
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade
from ProgressBarThreadGUI import ProgressBarThreadGUI
from RCEGraphicalDispatcher import RCEGraphicalTaskDispatcher
from RCEExceptionFrame import RCEExceptionFrame
from HMDCLog import exception_helper

class RCELaunchLaunchWindowFrame(wx.Frame):
  def __init__(self, *args, **kwds):
    # begin wxGlade: RCELaunchLaunchWindowFrame.__init__
    wx.Frame.__init__(self, *args) # **kwds)

    self.rceapps = kwds['rceapps']
    self.application = kwds['application']
    self.version = kwds['version']
    self.cpu = kwds['cpu']
    self.memory = kwds['memory']

    self._version = self.version if self.version else \
               self.rceapps.get_default_version(self.application)

    self._cpu = self.rceapps.cpu(self.application, self._version) if \
                self.cpu is None else self.cpu

    self._memory = (self.rceapps.memory(self.application,self._version) if \
                self.memory is None else self.memory) // 1024

    _app_name = "{0} {1}".format(self.application, self._version)

    self.RCEApplicationIcon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.rceapps.icon(self.application), wx.BITMAP_TYPE_ANY))
    self.HMDCApplicationNameVersion = wx.StaticText(self, wx.ID_ANY, _(_app_name))
    self.JobMemorySizeLabel = wx.StaticText(self, wx.ID_ANY, _("Memory (GB)"))
    self.JobMemoryTextCtrl = wx.TextCtrl(self, wx.ID_ANY, str(self._memory))
    # No node in the cluster currently has > 999GiB memory to reserve
    self.JobMemoryTextCtrl.SetMaxLength(3)
    # Make sure that only integers can be typed into this field
    self.JobMemoryTextCtrl.Bind(wx.EVT_CHAR, self.__validate_mem_cpu_entry)
    self.JobCpuRequestLabel = wx.StaticText(self, wx.ID_ANY, _("Cpu"))
    self.JobCpuTextCtrl = wx.TextCtrl(self, wx.ID_ANY, str(self._cpu))
    # Make sure that only integers can be teyped into this field
    self.JobCpuTextCtrl.Bind(wx.EVT_CHAR, self.__validate_mem_cpu_entry)
    # No one should try to acquire interactive job slots > 999 CPU(s)
    self.JobCpuTextCtrl.SetMaxLength(3)
    self.HelpBtn = wx.Button(self, wx.ID_ANY, _("Help"))
    self.RunJobBtn = wx.Button(self, wx.ID_ANY, _("Run"))
    self.RunJobBtn.Bind(wx.EVT_BUTTON, self.OnRunJobBtn)
    pub.subscribe(self.OnSubmitEvent, 'rce_submit.job_submitted')
    pub.subscribe(self.OnPollEvent, 'rce_submit.job_started')
    pub.subscribe(self.OnAttachEvent, 'rce_submit.xpra_attached')
    self.__set_properties()
    self.__do_layout()
    # end wxGlade

  def OnException(self, excpt):
    self.progress_bar_window.complete_task()
    self.dispatcher.join()
    self.Hide()
   
    RCEExceptionFrame(NONE, wx.ID_ANY, " ", msg=exception_helper(excpt)).Show()
 
    return
  def OnPollEvent(self, job_status=None, ad=None, excpt=None):
    
    def on_excpt():
      return OnException(excpt) if excpt is not None else end_current_task()
    
    def end_current_task():
      self.progress_bar_window.complete_task()
      self.dispatcher.join()
      return run_next_task()

    def run_next_task(parsed_ad=classad.parseOld(ad)):
      self.progress_bar_window.start_task("Attaching to job {0}".format(parsed_ad['HMDCApplicationName']))
      self.dispatcher = RCEGraphicalTaskDispatcher('attach_app', self.rceapps, self.jobid, ad)
      self.dispatcher.start() 

    return on_excpt()
 
  def OnAttachEvent(self, pid=None, exception=None):
    print "in event attached!"
    self.progress_bar_window.complete_task()
    self.dispatcher.join()
    # Quit application
    self.progress_bar_window.Destroy()
    self.Destroy()
    return

  def OnSubmitEvent(self, jobid = None):
    print "Received event. JobId = {0}".format(jobid)
    self.progress_bar_window.complete_task()
    self.dispatcher.join()
    self.progress_bar_window.start_task("Waiting for job to start") 
    # Run polling
    self.jobid = jobid
    self.dispatcher = RCEGraphicalTaskDispatcher('poll_app', self.jobid)
    self.dispatcher.start()

  def OnRunJobBtn(self, event):
    self.Hide()
    self.progress_bar_window = ProgressBarThreadGUI(None, wx.ID_ANY, " ", icon = self.rceapps.icon(self.application))
    self.progress_bar_window.Show()
    self.progress_bar_window.start_task("Submitting job")
    self.dispatcher = RCEGraphicalTaskDispatcher('run_app',
        self.application,
        self._version,
        self.rceapps.command(self.application, self._version),
        self.rceapps.args(self.application, self._version),
        self._memory*1024,
        self._cpu)
    self.dispatcher.start()

  def __set_properties(self):
    # begin wxGlade: RCELaunchLaunchWindowFrame.__set_properties
    self.SetTitle(_("Run RCE Powered Application Version"))
    self.HMDCApplicationNameVersion.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
    self.JobMemorySizeLabel.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
    self.JobMemorySizeLabel.SetToolTipString(_("Enter the desired memory"))
    self.JobCpuRequestLabel.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
    # end wxGlade

  def __do_layout(self):
    # begin wxGlade: RCELaunchLaunchWindowFrame.__do_layout
    LaunchWindowSizer = wx.FlexGridSizer(3, 2, 2, 6)
    LaunchWindowSizer.Add(self.RCEApplicationIcon, 0, 0, 0)
    LaunchWindowSizer.Add(self.HMDCApplicationNameVersion, 0, wx.ALIGN_CENTER_VERTICAL, 0)
    LaunchWindowSizer.Add(self.JobMemorySizeLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
    LaunchWindowSizer.Add(self.JobMemoryTextCtrl, 0, wx.EXPAND, 10)
    LaunchWindowSizer.Add(self.JobCpuRequestLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
    LaunchWindowSizer.Add(self.JobCpuTextCtrl, 0, wx.EXPAND, 10)
    LaunchWindowSizer.Add(self.HelpBtn, 0, wx.EXPAND, 0)
    LaunchWindowSizer.Add(self.RunJobBtn, 0, wx.EXPAND, 0)
    self.SetSizer(LaunchWindowSizer)
    LaunchWindowSizer.Fit(self)
    LaunchWindowSizer.AddGrowableCol(2)
    LaunchWindowSizer.AddGrowableCol(3)
    self.Layout()
    # end wxGlade

  def __validate_mem_cpu_entry(self, event):
    keycode = event.GetKeyCode()
    
    if chr(keycode) in "1234567890" or keycode in [13, 314, 316, 8, 127]:
      event.Skip()
      return
    else:
      return False 
