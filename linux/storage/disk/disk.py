# coding = utf-8
import linux
import re

class Disk:
	model = ""
	vendor = ""
	fw = ""
	sn = ""
	devName = ""
	smart = ""
	type = ""
	smartAttr = None
	

class DiskFromLsiSas3(Disk):
	def __init__(self, sn, name):
		self.sn = sn
		self.devName = name
	
	def fill_attrs(self):
		smart_str = linux.exe_shell("smartctl -a /dev/%s" % self.devName)
		smartx_str = linux.exe_shell("smartctl -x /dev/%s" % self.devName)
		self.smart = smartx_str
		self.fw = linux.exe_shell("")