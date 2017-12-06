# coding = utf-8
import linux
import re
import json
from linux import try_catch


class Disk:
	def __init__(self):
		self.model = ""
		self.vendor = ""
		self.fw = ""
		self.sn = ""
		self.dev_name = ""
		self.smart = ""
		self.type = ""
		self.smart_attr = {}


class DiskFromLsiSas3(Disk):
	def __init__(self, sn, name):
		Disk.__init__(self)
		self.sn = sn
		self.dev_name = name

	@try_catch
	def fill_attrs(self):
		smart_str = linux.exe_shell("smartctl -a /dev/%s" % self.dev_name)
		smartx_str = linux.exe_shell("smartctl -x /dev/%s" % self.dev_name)
		self.smart = smartx_str
		self.fw = linux.search_regex_strings_column(smart_str, "Firmware|Revision.+", ":", 1)[0].strip()
		self.vendor = linux.search_regex_strings_column(smart_str, "ATA|Vendor.+", ":", 1)[0].strip()
		self.sn = linux.search_regex_strings_column(smart_str, "Serial (N|n)umber.+", ":", 1)[0].strip()
		if "SAS" in smart_str:
			smart_str_arr = linux.search_regex_strings(smart_str, " *(write:|read:|verify:).+")
			for line in smart_str_arr:
				tmp = line.split()
				dict_tmp = {
					"errorEccFast": tmp[1],
					"errorEccDelayed": tmp[2],
					"errorEccByRereadsRewrite": tmp[3],
					"totalErrorsCorrected": tmp[4],
					"correctionAlgorithmInvocations": tmp[5],
					"byte10_9": tmp[6],
					"totalUncorrectedError": tmp[7]
				}
				self.smart_attr[tmp[0].replace(":", " ").strip()] = dict_tmp
			smart_str_arr = linux.search_regex_strings(
				self.smart,
				" +(Invalid DWORD)|(Running disparity)|(Loss of DWORD)|(Phy reset problem).+=.+"
			)
			i = 0
			dict_tmp = {}
			for it in smart_str_arr:
				tmp = it.split("=")
				dict_tmp[tmp[0]] = tmp[1]
				if 3 == i:
					self.smart_attr["channel0Error"] = dict_tmp
				if 7 == i:
					self.smart_attr["channel1Error"] = dict_tmp
				i += 1
		if "SATA" in smart_str:
			dict_tmp = linux.search_regex_strings(smart_str, "^( |[0-9])+.+[0-9]+ .+0x.+(In_the_past|-|FAILING_NOW) +[0-9]+")
			for line in dict_tmp:
				tmp = line.split()
				dict_tmp = {
					"ID": tmp[0],
					"FLAG": tmp[2],
					"VALUE": tmp[3],
					"WORST": tmp[4],
					"THRESH": tmp[5],
					"TYPE": tmp[6],
					"UPDATED": tmp[7],
					"WHEN_FAILED": tmp[8],
					"RAW_VALUE": tmp[9],
				}
				self.smart_attr[tmp[1]] = dict_tmp

	def to_json(self):
		struct = {
			"dev": self.dev_name,
			"model": self.model,
			"fw": self.fw,
			"SN": self.sn,
			"type": self.type,
			"vendor": self.vendor,
			"smart": self.smart_attr,
		}
		json_str = json.dumps(struct)
		return json_str


class DiskFromLsiSas2(DiskFromLsiSas3):
	def __init__(self, sn, name):
		DiskFromLsiSas3.__init__(self, sn, name)