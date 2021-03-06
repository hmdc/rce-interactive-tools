# -*- coding: UTF-8 -*-
#
# generated by wxGlade not found on Sun Oct 25 22:13:19 2015
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class RCEExceptionFrame(wx.Frame):
  def __init__(self, *args, **kwds):
    # begin wxGlade: RCEExceptionFrame.__init__
    wx.Frame.__init__(self, *args)
    self.RCEApplicationIcon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(kwds['icon'], wx.BITMAP_TYPE_ANY))
    self.ExceptionLabel = wx.StaticText(self, wx.ID_ANY, _("Encountered Error"))
    self.ErrorMessageTextCtrl = wx.TextCtrl(self, wx.ID_ANY, kwds['msg'], style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
    self.ExceptionOkBtn = wx.Button(self, wx.ID_EXIT, "")
    self.ExceptionOkBtn.Bind(wx.EVT_BUTTON, self.__exit_frame__)
    self.__set_properties()
    self.__do_layout()
    # end wxGlade

  def __exit_frame__(self, event):
    self.Destroy()

  def __set_properties(self):
    # begin wxGlade: RCEExceptionFrame.__set_properties
    self.SetTitle(_("Encountered Error"))
    self.SetSize((600, 350))
    self.ExceptionLabel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
    self.ErrorMessageTextCtrl.SetMinSize((276, 275))
    # end wxGlade

  def __do_layout(self):
    # begin wxGlade: RCEExceptionFrame.__do_layout
    ExceptionWindowParentSIzer = wx.BoxSizer(wx.VERTICAL)
    IconAndErorrNameSizer = wx.FlexGridSizer(1, 2, 0, 20)
    IconAndErorrNameSizer.Add(self.RCEApplicationIcon, 0, 0, 0)
    IconAndErorrNameSizer.Add(self.ExceptionLabel, 0, wx.ALIGN_CENTER, 0)
    ExceptionWindowParentSIzer.Add(IconAndErorrNameSizer, 1, 0, 0)
    ExceptionWindowParentSIzer.Add(self.ErrorMessageTextCtrl, 0, wx.EXPAND, 0)
    ExceptionWindowParentSIzer.Add(self.ExceptionOkBtn, 0, wx.ALIGN_CENTER, 0)
    self.SetSizer(ExceptionWindowParentSIzer)
    self.Layout()
    # end wxGlade

# end of class RCEExceptionFrame
