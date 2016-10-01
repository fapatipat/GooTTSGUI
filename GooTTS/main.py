import wx
app = wx.App(redirect=False)
from gui import interface
interface.window.Show()
app.MainLoop()