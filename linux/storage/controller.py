# coding = utf-8
import re
from .. import try_catch
import linux
from . import disk


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
	def scan_disk_name_sn():
		disks = linux.exe_shell("ls /dev|grep -P '^sd[a-z]+$'").splitlines()
		for d in disks:
			smart = linux.exe_shell("smartctl -i /dev/%s" % d)
		names = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +(?:[a-z]|[A-Z]|[0-9]| )+", " ", 0)
		sns = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +(?:[a-z]|[A-Z]|[0-9]| )+", " ", 1)
		vendors = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +(?:[a-z]|[A-Z]|[0-9]| )+", " ", 2)
		for i, e in enumerate(names):
			attr = [
				names[i],
				sns[i],
				vendors[i],
			]
			disks.append(attr)
		return disks


class LsiSas2Controller(Controller):
	def __init__(self, t_index, t_model):
		Controller.__init__(self, t_index, t_model)
		if re.match('SAS[0-9]{4}', t_model):
			self.model = t_model
		else:
			raise Exception("LsiSas2Controller model string is not available.")
		self.vendor = "LSI"
		self.index = t_index

	@try_catch
	def fill_attrs(self):
		sas2ircu_string = linux.exe_shell("sas2ircu %s display", self.index)
		fw_str = linux.get_match_sub_string(sas2ircu_string, 'Firmware.*(?:[0-9]+\\.)+[0-9]*')
		disk_name_sns = Controller.scan_from_sas23_disk_name_sn()
		tmp = fw_str.split(":")
		tmp_str = tmp[1].strip()
		if "" != tmp_str:
			self.fw = tmp_str
		else:
			self.fw = "null"
		for s in disk_name_sns:
			if re.match('.+(?:ATA|HGST).+', s[2]):
				self.disks.append(disk.DiskFromLsiSas2(s[1], s[0]))


class LsiSas3Controller(Controller):
	def __init__(self, t_index, t_model):
		Controller.__init__(self, t_index, t_model)
		if re.match('SAS[0-9]{4}', t_model):
			self.model = t_model
		else:
			raise Exception("LsiSas2Controller model string is not available.")
		self.vendor = "LSI"
		self.index = t_index

	@try_catch
	def fill_attrs(self):
		sas2ircu_string = linux.exe_shell("sas3ircu %s display", self.index)
		fw_str = linux.get_match_sub_string(sas2ircu_string, 'Firmware.*(?:[0-9]+\\.)+[0-9]*')
		disk_name_sns = Controller.scan_from_sas23_disk_name_sn()
		tmp = fw_str.split(":")
		tmp_str = tmp[1].strip()
		if "" != tmp_str:
			self.fw = tmp_str
		else:
			self.fw = "null"
		for s in disk_name_sns:
			if re.match('.+(?:ATA|HGST).+', s[2]):
				self.disks.append(disk.DiskFromLsiSas2(s[1], s[0]))
