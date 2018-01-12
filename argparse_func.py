# coding = utf-8
from linux.storage.phy import Phy
from linux.storage.controller import Controller
from linux.storage.disk import Disk
from linux.sysinfo import *
from linux import *
from setting import *
import time
import datetime
from numpy import matrix, array, linalg, random, amax, asscalar
import sys
import math
import threading


def list_dict(dict_a):
	if isinstance(dict_a, dict):
		for x in range(len(dict_a)):
			temp_key = dict_a.keys()[x]
			temp_value = dict_a[temp_key]
			if not isinstance(temp_value, dict):
				print("%s : %s" % (temp_key, temp_value))
			list_dict(temp_value)


def show_help():
	print(help_str)
	print(t_row)


def show_bios_info():
	'''show server's bios info.'''
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type bios")
	print(dmi_info)


def show_bios_date():
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type bios")
	print(search_regex_one_line_string_column(dmi_info, ".*Release Date:.*", ":", 1))


def show_bios_ver():
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type bios")
	print(search_regex_one_line_string_column(dmi_info, ".*Version:.*", ":", 1))


def show_mem_model():
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type memory")
	print(search_regex_one_line_string_column(dmi_info, ".*Part Number:.*", ":", 1))


def show_cpu_info():
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type processor")
	version = search_regex_strings_column(dmi_info, ".*Version:.*", ":", 1)
	cpu_model = version[0]
	cpu_num = len(version)
	core = search_regex_one_line_string_column(dmi_info, ".*Core Count:.*", ":", 1)
	thread_t = search_regex_one_line_string_column(dmi_info, ".*Thread Count:.*", ":", 1)
	print("cpu model: %s\ncpu num: %s\ncore per cpu: %s\nthread per cpu: %s" % (cpu_model, cpu_num, core, thread_t))


def show_err_phy():
	if not os.path.exists("/sys/class/sas_phy"):
		print("System has no sas_phys.")
		return
	row = PrettyTable()
	row.hrules = ALL
	row.vrules = ALL
	row.field_names = [
		"phy_name",
		"sas_address",
		"invalid_dword",
		"loss_of_dword_sync",
		"phy_reset_problem",
		"running_disparity",
	]
	err_phy_arr = Phy.scan_err_phys()
	for i in err_phy_arr:
		row.add_row([
			i.phy_name,
			i.sas_address,
			i.invalid_dword_count,
			i.loss_of_dword_sync_count,
			i.phy_reset_problem_count,
			i.running_disparity_error_count
		])
	print(row)


def show_err_disk():
	err_disks_dict = Disk.get_err_disk_dict()
	err_disk_json = json.dumps(err_disks_dict, indent=1)
	print(err_disk_json)


def gpu_monitor():
	while True:
		Bmc.monitor_gpu_temp()
		time.sleep(4)


def write_all_log():
	log_dict = Log.get_all_log()
	phys_dict = Phy.phys_to_dict()
	controller_disk_dict = Controller.get_controllers_disks_all_dict()
	t_dict = {
		"get_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'''BMC and sys log'''
		"sys_log": log_dict,
		"phys_log": phys_dict,
		"controller_disk_log": controller_disk_dict
	}
	if not os.path.exists(log_path):
		os.mkdir(log_path)
	json_path = os.path.join(log_path, "log.json")
	dict_to_json_file(t_dict, json_path)


def upload_logfile_to_server():
	json_path = os.path.join(log_path, "log.json")
	re = exe_shell("sshpass -p 000000 scp %s root@%s:%s" % (json_path, server_ip, server_logpath))
	if "" == re:
		print("Upload %s success." % json_path)
	else:
		print("Upload failed. Cannot connect to the server!")


def linpack_run():
	# (N*N*2*8.00+N*5)/1024/1024/1024=mem_size
	# a = malloc(n * n * sizeof(double));
	# a2 = malloc(n * n * sizeof(double));
	# b = malloc(n * sizeof(double));
	# b2 = malloc(n * sizeof(double));
	# x = malloc(n * sizeof(double));
	# r = malloc(n * sizeof(double));
	# ipvt = malloc(n * sizeof(int));
	tmp = int(exe_shell("free -g|grep Mem|awk '{print$7}'"))
	mem_size = int(tmp * 0.85)
	N = int((math.sqrt(25 + 64 * 1024 * 1024 * 1024 * mem_size) - 5) / 32)
	eps = 2.22e-16
	ops = (2.0 * N) * N * N / 3.0 + (2.0 * N) * N
	A = random.random_sample((N, N)) - 0.5
	B = A.sum(axis=1)
	A = matrix(A)
	B = matrix(B.reshape((N, 1)))
	na = amax(abs(A.A))
	t = time.time()

	while True:
		X = linalg.solve(A, B)
		t = time.time() - t
		R = A * X - B
		Rs = asscalar(max(abs(R.A)))
		nx = asscalar(max(abs(X)))
		print("Residual is ", Rs)
		print("Normalised residual is ", Rs / (N * na * nx * eps))
		print("Machine epsilon is ", eps)
		print("x[0]-1 is ", asscalar(X[0]) - 1)
		print("x[n-1]-1 is ", asscalar(X[N - 1]) - 1)


def run_linpack(r_t=-1):
	t2 = threading.Thread(target=linpack_run)
	t2.setDaemon(True)
	t2.start()
	r_t = int(r_t) * 60
	if r_t != -60:
		while r_t > 0:
			r_t -= 1
			time.sleep(1)
	else:
		t2.join()
