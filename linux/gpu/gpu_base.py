# coding = utf-8
import linux


class Gpu:
	def __init__(
			self,
			attr_list
	):
		self.name = attr_list[0]
		self.fan_util = attr_list[1]
		self.temp = attr_list[2]
		self.cur_power = attr_list[3]
		self.total_power = attr_list[4]
		self.mem_util = attr_list[5]
		self.total_mem = attr_list[6]
		self.gpu_util = attr_list[7]
		self.bus_id = attr_list[8]
		self.minor = attr_list[9]
		self.vbios = attr_list[10]
		self.sn = attr_list[11]
	
	@staticmethod
	def check_driver():
		re = int(linux.exe_shell("nvidia-smi -h 2> /dev/zero | wc -l"))
		if 0 == re:
			return False
		else:
			return True
	
	@staticmethod
	def get_all_gpus():
		gpu_list = []
		if not Gpu.check_driver():
			print("Nvidia driver is not install.")
			return
		nvsmi_text = linux.exe_shell("nvidia-smi -a")
		tmp_list = nvsmi_text.split('\n\n')
		gpu_info_list = tmp_list[2:-1]
		kv = [
			"Product Name.*:.*",
			"Fan Speed.*:.*",
			"GPU Current Temp.*:.*",
			"Power Draw.*:.*",
			"  Power Limit.*:.*",
			"Memory.*:.*%.*",
			"Total.*: [0-9]{4,} MiB",
			"Gpu.*:.*%.*",
			"Bus Id.*\.[0-9]",
			"Minor.*:.*",
			"VBIOS.*:.*",
			"Serial Number.*:.*"
		]
		for gpu_info in gpu_info_list:
			result = []
			for k in kv:
				result.append(linux.search_regex_one_line_string_column(gpu_info, k, ":", 1).strip())
			gpu = Gpu(result)
			gpu_list.append(gpu)
		return gpu_list
