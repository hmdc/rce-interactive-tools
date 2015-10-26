# -*- coding: UTF-8 -*-
#
# generated by wxGlade not found on Sun Oct 25 22:13:19 2015
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class ProgressBarThreadGUI(wx.Frame):
  def __init__(self, *args, **kwds):
    # begin wxGlade: ProgressBarThreadGUI.__init__
    wx.Frame.__init__(self, *args, **kwds)
    self.RCEApplicationIcon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("/mnt/deployment/hmdc-admin/shared/system/xdg/HMDC-icon-octave.png", wx.BITMAP_TYPE_ANY))
    self.RCECurrentTask = wx.StaticText(self, wx.ID_ANY, _("Current Task"))
    self.CancelJobTaskBtn = wx.Button(self, wx.ID_CANCEL, "")

    self.__set_properties()
    self.__do_layout()
    # end wxGlade

  def __set_properties(self):
    # begin wxGlade: ProgressBarThreadGUI.__set_properties
    self.SetTitle(_("Current Task"))
    self.SetSize((350, 105))
    self.RCECurrentTask.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
    # end wxGlade

  def __do_layout(self):
    # begin wxGlade: ProgressBarThreadGUI.__do_layout
    ProgressBarThreadGuiParentSizer = wx.BoxSizer(wx.VERTICAL)
    ProgressBarIconAndTaskNameSizer = wx.FlexGridSizer(1, 2, 0, 0)
    ProgressBarIconAndTaskNameSizer.Add(self.RCEApplicationIcon, 0, 0, 0)
    ProgressBarIconAndTaskNameSizer.Add(self.RCECurrentTask, 0, wx.ALIGN_CENTER, 0)
    ProgressBarIconAndTaskNameSizer.AddGrowableCol(0)
    ProgressBarIconAndTaskNameSizer.AddGrowableCol(1)
    ProgressBarThreadGuiParentSizer.Add(ProgressBarIconAndTaskNameSizer, 1, 0, 0)
    ProgressBarThreadGuiParentSizer.Add((20, 20), 0, 0, 0)
    ProgressBarThreadGuiParentSizer.Add(self.CancelJobTaskBtn, 0, wx.ALIGN_CENTER, 0)
    self.SetSizer(ProgressBarThreadGuiParentSizer)
    self.Layout()
    # end wxGlade

# end of class ProgressBarThreadGUI