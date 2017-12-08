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
		cons = []
		if "" != sas2_con.strip():
			indexs = linux.search_regex_strings_column(sas2_con, "[0-9]+ *SAS[0-9]{4}.*", " ", 0)
			con_str = linux.search_regex_strings(sas2_con, "SAS[0-9]{4}")
			for i in range(len(indexs)):
				c = LsiSas2Controller(int(indexs[i]), con_str[i])
				c.fill_attrs()
				cons.append(c)
		if "" != sas3_con.strip():
			indexs = linux.search_regex_strings_column(sas3_con, "[0-9]+ *SAS[0-9]{4}.*", " ", 0)
			con_str = linux.search_regex_strings(sas3_con, "SAS[0-9]{4}")
			for i in range(len(indexs)):
				c = LsiSas3Controller(int(indexs[i]), con_str[i])
				c.fill_attrs()
				cons.append(c)
		if "" != mega_raid_con.strip():
			indexs = linux.search_regex_strings_column(sas2_con, ".*SAS[0-9]{4}.*", " ", 0)
			con_str = linux.search_regex_strings(sas2_con, "SAS[0-9]{4}")
			for i in range(len(indexs)):
				c = LsiSas2Controller(int(indexs[i]), con_str[i])
				c.fill_attrs()
				cons.append(c)
		return cons
	
	@staticmethod
	def scan_disk_name_sn():
		disks = linux.exe_shell("ls /dev|grep -P '^sd[a-z]+$'").splitlines()
		disks_attr = []
		for d in disks:
			attr_arr = disk.Disk.get_from_sas_disk_simple_attr(d)
			disks_attr.append(attr_arr)
		return disks_attr


class LsiSas2Controller(Controller):
	def __init__(self, t_index, t_model):
		Controller.__init__(self)
		if re.match('SAS[0-9]{4}', t_model):
			self.model = t_model
		else:
			raise Exception("LsiSas2Controller model string is not available.")
		self.vendor = "LSI"
		self.index = t_index

	@try_catch
	def fill_attrs(self):
		sas2ircu_string = linux.exe_shell("sas2ircu %d display" % self.index)
		fw_str = linux.get_match_sub_string(sas2ircu_string, 'Firmware.*(?:[0-9]+\\.)+[0-9]*')
		sn_list = linux.search_regex_strings_column(sas2ircu_string, "^ +Serial No.+", ":", 1)
		disk_name_sns = Controller.scan_disk_name_sn()
		tmp = fw_str.split(":")
		tmp_str = tmp[1].strip()
		if "" != tmp_str:
			self.fw = tmp_str
		else:
			self.fw = "null"
		for s in disk_name_sns:
			if s["sn"] in sn_list:
				d = disk.DiskFromLsiSas2(s["sn"], s["name"])
				d.fill_attrs()
				self.disks.append(d)


class LsiSas3Controller(Controller):
	def __init__(self, t_index, t_model):
		Controller.__init__(self)
		if re.match('SAS[0-9]{4}', t_model):
			self.model = t_model
		else:
			raise Exception("LsiSas2Controller model string is not available.")
		self.vendor = "LSI"
		self.index = t_index

	@try_catch
	def fill_attrs(self):
		sas3ircu_string = linux.exe_shell("sas3ircu %d display" % self.index)
		fw_str = linux.get_match_sub_string(sas3ircu_string, "Firmware.*(?:[0-9]+\\.)+[0-9]*")
		sn_list = linux.search_regex_strings_column(sas3ircu_string, "^ +Serial No.+", ":", 1)
		disk_name_sns = Controller.scan_disk_name_sn()
		tmp = fw_str.split(":")
		tmp_str = tmp[1].strip()
		if "" != tmp_str:
			self.fw = tmp_str
		else:
			self.fw = "null"
		for s in disk_name_sns:
			if s["sn"] in sn_list:
				d = disk.DiskFromLsiSas3(s["sn"], s["name"])
				d.fill_attrs()
				self.disks.append(d)
