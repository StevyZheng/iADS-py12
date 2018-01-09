# coding = utf-8
from linux import *
from linux.gpu.gpu_base import Gpu

fan_mode = {
	"Optimal": "2",
	"Full": "1",
	"Heavy": "4"
}

gpu_critical_temp = 75


class Bmc:
	ip_addr = ""
	mac = ""
	fan_mode = 2
	
	def __init__(self):
		pass

	@staticmethod
	def get_bmc_log():
		bmc_log = exe_shell("ipmicfg -sel")
		bmc_log_dict = {
			"bmc_log": bmc_log
		}
		return bmc_log_dict

	@staticmethod
	def get_fan_mode():
		return exe_shell("ipmicfg -fan | grep 'Fan Speed' | awk '{print$7}'")
		
	@staticmethod
	def set_fan_model(mode):
		exe_shell("ipmicfg -fan %s" % fan_mode[mode])
	
	@staticmethod
	def monitor_gpu_temp():
		gpus = Gpu.get_all_gpus()
		max = 0
		min = 0
		for i in gpus:
			if int(i.temp.split()[0]) > gpu_critical_temp:
				if max == 0:
					Bmc.set_fan_model("Full")
					max = 1
			else:
				min += 1
		if len(gpus) == min:
			Bmc.set_fan_model("Optimal")
			max = 0
			

class SysInfo:
	def __init__(self):
		self.dmesg_err = {}
		self.messages_err = {}
		self.mce_err = {}
		self.bmc_err = {}
		self.dmesg_reg = ["error", "Call Trace", "failed", "segfault", ]
		self.dmesg = ""
		self.messages = ""
		self.lsscsi = ""
		self.dmidecode = ""
		self.lsblk = ""
		self.lspci = ""

	@staticmethod
	def get_sys_log():
		sysinfo = SysInfo()
		sysinfo.fill_attr()
		sys_info_dict = {
			"dmesg": sysinfo.dmesg,
			"messages": sysinfo.messages,
			"lsscsi": sysinfo.lsscsi,
			"dmidecode": sysinfo.dmidecode,
			"lspci": sysinfo.lspci,
			"lsblk": sysinfo.lsblk
		}
		return sys_info_dict

	def fill_attr(self):
		self.fill_dmesg()
		self.fill_messages()
		self.fill_lsblk()
		self.fill_lsscsi()
		self.fill_lspci()
		self.fill_dmidecode()

	def fill_dmesg(self):
		if bin_exists("dmesg"):
			self.dmesg = exe_shell("dmesg")
		else:
			raise Exception("dmesg not exists!")

	def fill_messages(self):
		self.messages = read_file("/var/log/messages")

	def fill_lsscsi(self):
		if bin_exists("lsscsi"):
			self.lsscsi = exe_shell("lsscsi")
		else:
			raise Exception("lsscsi not exists!")

	def fill_lsblk(self):
		if bin_exists("lsblk"):
			self.lsblk = exe_shell("lsblk")
		else:
			raise Exception("lsblk not exists!")

	def fill_lspci(self):
		if bin_exists("lspci"):
			self.lspci = exe_shell("lspci")
		else:
			raise Exception("lspci not exists!")

	def fill_dmidecode(self):
		if bin_exists("dmidecode"):
			self.dmidecode = exe_shell("dmidecode")
		else:
			raise Exception("dmidecode is not exists!")

	def analyze_dmesg(self):
		pass


class Log:
	def __init__(self):
		pass

	@staticmethod
	def get_all_log():
		bmc_log = Bmc.get_bmc_log()
		sys_log = SysInfo.get_sys_log()
		log_dict = {
			"bmc_log": bmc_log,
			"sys_log": sys_log
		}
		return log_dict

	@staticmethod
	def get_log_json():
		t_dict = Log.get_all_log()
		return dict_to_json(t_dict)

	@staticmethod
	def store_log_json(t_file_path):
		t_dict = Log.get_all_log()
		dict_to_json_file(t_dict, t_file_path)
