# coding = utf-8
from linux import exe_shell
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
	
	def analyze_dmesg(self):
		pass
