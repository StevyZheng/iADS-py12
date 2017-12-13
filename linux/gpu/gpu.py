# coding = utf-8
import linux


class Gpu:
	def __init__(
			self,
			t_id,
			t_name,
			t_fan_util,
			t_temp,
			t_perf,
			t_cur_power,
			t_total_power,
			t_cur_mem,
			t_total_mem,
			t_gpu_util,
			t_bus_id
	):
		self.id = t_id
		self.name = t_name
		self.fan_util = t_fan_util
		self.temp = t_temp
		self.perf = t_perf
		self.cur_power = t_cur_power
		self.total_power = t_total_power
		self.cur_mem = t_cur_mem
		self.total_mem = t_total_mem
		self.gpu_util = t_gpu_util
		self.bus_id = t_bus_id

	@staticmethod
	def get_all_gpus():
		nv_smi_text = linux.exe_shell("nvidia-smi")
		if "Driver Version" not in nv_smi_text:
			raise Exception("Cannot get GPU info!")
			print("Cannot get GPU info!")
			return
		gpu_list = linux.search_regex_strings(
			nv_smi_text,
			"\|(?:( +[0-9]+ +.+\|.+\|.+|)|(\|.+C.+W./.+W\|.+/.+\|.+[0-9]+%.+\|))"
		)
		i = 0
		for line in nv_smi_text:
			i += 1
