#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade not found on Sun Oct 25 22:13:19 2015
#

# This is an automatically generated file.
# Manual changes will be overwritten without warning!

import wx
import gettext
from RCELaunchLaunchWindowFrame import RCELaunchLaunchWindowFrame

class RceSubmitLaunch(wx.App):
  def __init__(self, *args, **kwargs):
    self.rceapps = kwargs['rceapps']
    self.application = kwargs['application']
    self.version = kwargs['version']
    self.memory = kwargs['memory']
    self.cpu = kwargs['cpu']
    super(RceSubmitLaunch, self).__init__(*args)
    return

  def OnInit(self):
    gettext.install("RceGraphicalClient")
    wx.InitAllImageHandlers()
    LaunchWindow = RCELaunchLaunchWindowFrame(None, wx.ID_ANY, "",
	rceapps = self.rceapps,
        application = self.application,
        version = self.version,
        memory = self.memory,
        cpu = self.cpu)
    self.SetTopWindow(LaunchWindow)
    LaunchWindow.Show()
    return 1

  def __call__(self):
    gettext.install("RceSubmit")
    self.MainLoop()
