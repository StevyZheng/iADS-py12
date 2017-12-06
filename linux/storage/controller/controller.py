# coding = utf-8
import re
from linux import try_catch
import linux
from linux.storage.disk import disk
from linux.storage.controller import scan_from_sas23_disk_name_sn


class Controller:
	def __init__(self):
		self.model = ""
		self.index = -1
		self.vendor = ""
		self.fw = ""
		self.disks = []


class LsiSas2Controller(Controller):
	def __init__(self, index, model):
		Controller.__init__(self, index, model)
		if re.match("SAS[0-9]{4}", model):
			self.model = model
		else:
			raise Exception("LsiSas2Controller model string is not available.")
		self.vendor = "LSI"
		self.index = index

	@try_catch
	def fill_attrs(self):
		sas2ircu_string = linux.exe_shell("sas2ircu %s display", self.index)
		fw_str = linux.get_match_sub_string(sas2ircu_string, "Firmware.*([0-9]+\\.)+[0-9]*")
		disk_name_sns = scan_from_sas23_disk_name_sn()
		tmp = fw_str.split(":")
		tmp_str = tmp[1].strip()
		if "" != tmp_str:
			self.fw = tmp_str
		else:
			self.fw = "null"
		for s in disk_name_sns:
			if re.match(".+(ATA|HGST).+", s[2]):
				self.disks.append(disk.DiskFromLsiSas2(s[1], s[0]))