from random import randint
import sound_lib
from sound_lib import output
from sound_lib import stream
from gtts import gTTS
import tempfile
import application
import wx
o=output.Output()
class MainGui(wx.Frame):
	def __init__(self, title):
		self.temp=tempfile.gettempdir()
		wx.Frame.__init__(self, None, title=title, size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Text")
		self.text = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.button = wx.Button(self.panel, wx.ID_DEFAULT, "&Speak")
		self.button.SetDefault()
		self.button.Bind(wx.EVT_BUTTON, self.OnSpeak)
		self.main_box.Add(self.button, 0, wx.ALL, 10)
		self.stopbutton = wx.Button(self.panel, -1, "&Stop")
		self.stopbutton.Bind(wx.EVT_BUTTON, self.OnStop)
		self.main_box.Add(self.stopbutton, 0, wx.ALL, 10)
		self.mp3button = wx.Button(self.panel, -1, "Speak to MP3 &File")
		self.mp3button.Bind(wx.EVT_BUTTON, self.OnSpeakMP3)
		self.main_box.Add(self.mp3button, 0, wx.ALL, 10)
		self.exitbutton = wx.Button(self.panel, -1, "E&xit")
		self.exitbutton.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.exitbutton, 0, wx.ALL, 10)

		self.panel.Layout()

	def OnSpeak(self, event):
		a=self.speak_wrapper(self.text.GetValue())
		self.s=self.speak_file(a)

	def OnStop(self, event):
		self.stop(self.s)

	def OnSpeakMP3(self, event):
		openFileDialog = wx.FileDialog(self, "Save the MP3 file", "", "", "Audio Files (*.mp3)|*.mp3", wx.FD_SAVE)
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return False
		self.filename= openFileDialog.GetPath()
		self.speak_wrapper(self.text.GetValue(),self.filename)

	def speak_wrapper(self,txt,file=""):
		if file=="":
			file=self.temp+"/"+str(randint(1,50000000))+".mp3"

		tts = gTTS(text=txt, lang='en')
		tts.save(file)
		return file

	def speak_file(self,file):
		s=stream.FileStream(file=file)
		s.play()
		return s

	def stop(self,s):
		s.stop()

	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()
global window
window=MainGui(application.name+" V"+application.version)