# coding = utf-8


class SysInfo:
	def __init__(self):
		self.dmesg_err = {}
		self.messages_err = {}
		self.mce_err = {}
		self.bmc_err = {}
		self.dmesg_reg = ["error", "Call Trace", "failed", "segfault", ]
	
	def analyze_dmesg(self):
		pass
