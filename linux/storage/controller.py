# coding = utf-8
import re
from .. import try_catch
import linux
from . import disk
from . import scan_from_sas23_disk_name_sn


class Controller:
	def __init__(self):
		self.model = ""
		self.index = -1
		self.vendor = ""
		self.fw = ""
		self.disks = []
	
	@staticmethod
	def scan_controller():
		sas2_con = linux.exe_shell("sas2ircu list|grep -P 'SAS[0-9]{4}'")
		sas3_con = linux.exe_shell("sas3ircu list|grep -P 'SAS[0-9]{4}'")
		mega_raid_con = linux.exe_shell("storcli show|grep LSI")
		if "" == sas2_con.strip():
			indexs = linux.search_regex_strings_column(sas2_con, ".*SAS[0-9]{4}.*", " ", 0)
			con_str = linux.search_regex_strings(sas2_con, "SAS[0-9]{4}")
	
	@staticmethod
	def scan_from_sas23_disk_name_sn():
		disks = []
		tmp = linux.exe_shell("lsblk -o NAME,SERIAL,VENDOR")
		names = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +([a-z]|[A-Z]|[0-9]| )+", " ", 0)
		sns = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +([a-z]|[A-Z]|[0-9]| )+", " ", 1)
		vendors = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +([a-z]|[A-Z]|[0-9]| )+", " ", 2)
		for i, e in enumerate(names):
			attr = [
				names[i],
				sns[i],
				vendors[i],
			]
			disks.append(attr)
		return disks


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
