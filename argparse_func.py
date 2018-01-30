# coding = utf-8
from linux.storage.phy import Phy
from linux.storage.controller import Controller
from linux.storage.disk import Disk
from linux.sysinfo import *
from linux import *
from setting import *
import time
import string
import datetime
from numpy import matrix, linalg, random, amax, asscalar
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


@try_catch
def write_a(file_t, str_t):
	with open(file_t, "a") as fp:
		fp.write(str_t)


def log_monitor():
	start_log_path = "/var/log/start-iads-monitor-log.log"
	log_path = "/var/log/iads-monitor-log.log"
	start_time_t = exe_shell("date")

	start_lsi_str = exe_shell("lsiutil.x86_64_171  -p  1  -a  64,1,,debuginfo,exit,0")
	start_hba_str = exe_shell("lsiutil.x86_64_171  -p  1  -a  65,,'pl dbg',exit,0")
	start_dmesg_str = exe_shell("dmesg|grep -iP '((i/o error)|(sector [0-9]+))'")
	start_messages_str = exe_shell("cat /var/log/messages|grep -iP '((i/o error)|(sector [0-9]+))'")
	start_str = "\ntime:\n%s\ndmesg:\n%s\n\nmessage:\n%s\n\nlsiutils debuginfo:\n%s\n\nlsiutils_pl dbg:\n%s\n\n" % (start_time_t, start_dmesg_str, start_messages_str, start_lsi_str, start_hba_str)
	with open(start_log_path, "a") as fp:
		fp.write(start_str)
	print("Start_log is OK. path: /var/log/start-iads-monitor-log.log \n")

	i_times = 0
	phy_t_list = Phy.scan_phys_attr()
	collect = False
	while True:
		g_lsi_str = exe_shell("lsiutil.x86_64_171  -p  1  -a  64,1,,debuginfo,exit,0")
		g_hba_str = exe_shell("lsiutil.x86_64_171  -p  1  -a  65,,'pl dbg',exit,0")
		dmesg_str = exe_shell("dmesg|grep -iP '((i/o error)|(sector [0-9]+))'")
		phy_list = Phy.scan_phys_attr()
		for i in range(0, len(phy_list)):
			if len(phy_t_list) != len(phy_list):
				collect = True
				continue
			if phy_list[i].invalid_dword_count != phy_t_list[i].invalid_dword_count or phy_list[
				i].loss_of_dword_sync_count != phy_t_list[i].loss_of_dword_sync_count:
				collect = True
			if phy_list[i].phy_reset_problem_count != phy_t_list[i].phy_reset_problem_count or phy_list[
				i].running_disparity_error_count != phy_t_list[i].running_disparity_error_count:
				collect = True
		if not collect:
			continue
		print("Phy err increased.Start collect logs to /var/log/iads-monitor-log.log......")
		phy_t_list = phy_list

		messages_str = exe_shell("cat /var/log/messages|grep -iP '((i/o error)|(sector [0-9]+))'")
		i_times += 1
		time_t = exe_shell("date")
		lsi_str = exe_shell("lsiutil.x86_64_171  -p  1  -a  64,1,,debuginfo,exit,0")
		hba_str = exe_shell("lsiutil.x86_64_171  -p  1  -a  65,,'pl dbg',exit,0")
		tmp_str = "\n%s\ndmesg:\n%s\nmessages:\n%s\nbefore_lsi_str:\n%s\nafter_lsi_str:\n%s\nbefore_hba_lig:\n%s\nafter_hba_log:\n%s\n" % (
		time_t, dmesg_str, messages_str, g_lsi_str, lsi_str, g_hba_str, hba_str)
		with open(log_path, "a") as fp:
			fp.write(tmp_str)
			fp.writelines("\n\n\nsmart info:\n")
		for case in ("", "a", "b", ):
			for i in string.lowercase:
				write_a(log_path, "\nsd%s%s\n" % (case, i))
				exe_shell("smartctl -x /dev/sd%s%s >> /var/log/iads-monitor-log.log" % (case, i))
		exe_shell("lsigetlunix.sh")
		break


def collect_err_log():
	err_sysinfo = SysInfo().analyze_dmesg()
	phys_err_dict = Phy.err_phys_to_dict()
	disk_err_dict = Disk.get_err_disk_dict()
	t_dict = {
		"get_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		"sys_err_log": err_sysinfo,
		"phys_err_log": phys_err_dict,
		"disk_err_log": disk_err_dict
	}
	return t_dict


def collect_all_log():
	log_dict = Log.get_all_log()
	phys_dict = Phy.phys_to_dict()
	disk_log = Controller.get_controllers_disks_all_dict()
	t_dict = {
		"get_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		"sys_log": log_dict,
		"phys_log": phys_dict,
		"disk_log": disk_log
	}
	return t_dict


def write_all_log():
	t_dict = collect_all_log()
	if not os.path.exists(log_path):
		os.mkdir(log_path)
	json_path = os.path.join(log_path, "log.json")
	dict_to_json_file(t_dict, json_path)


def print_err_log():
	t_dict = collect_err_log()
	print(dict_to_json(t_dict))


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


def run_reboot(sec):
	reboot(sec)
	while True:
		user_in = raw_input("Reboot now ?  [y/n]")
		if "y" == user_in:
			exe_shell("reboot")
		elif "n" == user_in:
			break


def clean_reboot():
	clean_reboot_log()


def rm_reboot():
	rm_reboot_t()
