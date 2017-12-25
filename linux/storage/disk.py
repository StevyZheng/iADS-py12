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

	@staticmethod
	@try_catch
	def get_from_sas_disk_smart_i_str(disk_name):
		return linux.exe_shell("smartctl -i /dev/%s" % disk_name)

	@staticmethod
	def get_from_sas_disk_simple_attr(disk_name):
		smart = Disk.get_from_sas_disk_smart_i_str(disk_name)
		model = linux.search_regex_one_line_string_column(smart, "(?:Device Model|Product):.+", ":", 1).strip()
		sn = linux.search_regex_one_line_string_column(smart, "Serial (?:N|n)umber.+", ":", 1).strip()
		vendor = linux.search_regex_one_line_string_column(smart, "(?:ATA|Vendor).+", ":", 1).strip()
		return {
			"name": disk_name,
			"model": model,
			"sn": sn,
			"vendor": vendor
		}

	@staticmethod
	def get_all_disk():
		disks = []
		disks_lines = linux.exe_shell("lsblk -o NAME,VENDOR|grep '^sd*'")
		for line in disks_lines.splitlines():
			disk_t = line.split()
			if "LSI" not in disk_t[1]:
				disks.append(disk_t[0])
		ds = []
		for i in disks:
			d_t = DiskFromLsiSas3("", i)
			d_t.fill_attrs()
			ds.append(d_t)
		return ds

	@staticmethod
	def __if_smart_err(disk_oj):
		if "SAS" in disk_oj.smart:
			if int(disk_oj.smart_attr["channel0Error"]["Invalid DWORD count"]) > 0 or \
				int(disk_oj.smart_attr["channel0Error"]["Running disparity error count"]) > 0 or \
				int(disk_oj.smart_attr["channel0Error"]["Loss of DWORD synchronization"]) > 0 or \
				int(disk_oj.smart_attr["channel0Error"]["Phy reset problem"]) > 0 or \
				int(disk_oj.smart_attr["channel1Error"]["Invalid DWORD count"]) > 0 or \
				int(disk_oj.smart_attr["channel1Error"]["Running disparity error count"]) > 0 or \
				int(disk_oj.smart_attr["channel1Error"]["Loss of DWORD synchronization"]) > 0 or \
				int(disk_oj.smart_attr["channel1Error"]["Phy reset problem"]) > 0:
				return True
			else:
				return False
		if "SATA" in disk_oj.smart:
			pass

	@staticmethod
	def get_err_disk_dict():
		err_disk_dict = {}
		disks = Disk.get_all_disk()
		for i in disks:
			if Disk.__if_smart_err(i):
				struct = {
					"dev": i.dev_name,
					"model": i.model,
					"fw": i.fw,
					"SN": i.sn,
					"type": i.type,
					"vendor": i.vendor,
					"smart": i.smart_attr,
				}
				err_disk_dict[i.dev_name] = struct
		return err_disk_dict


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
		self.model = linux.search_regex_one_line_string_column(smart_str, "(?:Device Model|Product):.+", ":", 1).strip()
		self.fw = linux.search_regex_one_line_string_column(smart_str, "(?:Firmware|Revision).+", ":", 1).strip()
		self.vendor = linux.search_regex_one_line_string_column(smart_str, "(?:ATA|Vendor).+", ":", 1).strip()
		self.sn = linux.search_regex_one_line_string_column(smart_str, "Serial (?:N|n)umber.+", ":", 1).strip()
		if "SAS" in smart_str:
			self.type = "SAS"
			smart_str_arr = linux.search_regex_strings(smart_str, " *(?:write:|read:|verify:).+")
			for line in smart_str_arr:
				tmp = line.split()
				dict_tmp = {
					"errorEccFast": tmp[1].strip(),
					"errorEccDelayed": tmp[2].strip(),
					"errorEccByRereadsRewrite": tmp[3].strip(),
					"totalErrorsCorrected": tmp[4].strip(),
					"correctionAlgorithmInvocations": tmp[5].strip(),
					"byte10_9": tmp[6].strip(),
					"totalUncorrectedError": tmp[7].strip()
				}
				self.smart_attr[tmp[0].replace(":", " ").strip()] = dict_tmp
			smart_str_arr = linux.search_regex_strings(
				self.smart,
				"(?:Invalid DWORD|Running disparity|Loss of DWORD|Phy reset problem).+=.+"
			)
			i = 0
			dict_tmp = {}
			for it in smart_str_arr:
				tmp = it.split("=")
				dict_tmp[tmp[0].strip()] = tmp[1].strip()
				if 3 == i:
					self.smart_attr["channel0Error"] = dict_tmp
					dict_tmp = {}
				if 7 == i:
					self.smart_attr["channel1Error"] = dict_tmp
					dict_tmp = {}
				i += 1
		if "SATA" in smart_str:
			self.type = "SATA"
			dict_tmp = linux.search_regex_strings(smart_str, "^( |[0-9])+.+[0-9]+ .+0x.+(In_the_past|-|FAILING_NOW) +[0-9]+")
			for line in dict_tmp:
				tmp = line.split()
				dict_tmp = {
					"ID": tmp[0].strip(),
					"FLAG": tmp[2].strip(),
					"VALUE": tmp[3].strip(),
					"WORST": tmp[4].strip(),
					"THRESH": tmp[5].strip(),
					"TYPE": tmp[6].strip(),
					"UPDATED": tmp[7].strip(),
					"WHEN_FAILED": tmp[8].strip(),
					"RAW_VALUE": tmp[9].strip(),
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
		json_str = json.dumps(struct, indent=1)
		return json_str


class DiskFromLsiSas2(DiskFromLsiSas3):
	def __init__(self, sn, name):
		DiskFromLsiSas3.__init__(self, sn, name)
