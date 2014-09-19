#!/usr/local/bin/python
import htcondor
import classad
import wx
from getpass import getuser

# Proof of concept using condor API
my_username = getuser()
my_job_username = my_username + "@hmdc.harvard.edu"
condor_collector = htcondor.Collector("dev-cod6-head.priv.hmdc.harvard.edu")

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'rce-icon.png'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	# SELF JOBS
	self.jobs = {}

	# START A TEST TIMER
        self.query_jobs_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_query_jobs_timer)
        self.query_jobs_timer.Start(750)

    def on_query_jobs_timer(self, timer):
	'''This function collects all ClassAds which I own as a user and only requests the
        Machine and JobID ClassAd'''
	ads = condor_collector.query(htcondor.AdTypes.Startd,
		'RemoteUser =?= "' + my_job_username + '"',
	        ['Machine', 'JobId'])

	_jobs = {}

	for ad in ads:
		_jobs[ad.get('JobId')] = { 'machine': ad.get('Machine') }

	self.jobs = _jobs

    def CreatePopupMenu(self):
        menu = wx.Menu()

	for job,ad in self.jobs.items():
            create_menu_item(menu, job + '/' + ad['machine'], self.on_exit)

        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print 'Tray icon was left-clicked.'

    def on_hello(self, event):
        print 'Hello, world!'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)


def main():
    app = wx.PySimpleApp()
    TaskBarIcon()
    app.MainLoop()


if __name__ == '__main__':
    main()
