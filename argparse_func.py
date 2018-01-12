# coding = utf-8
from prettytable import *
from linux.storage.phy import Phy
from linux.storage.controller import Controller
from linux.storage.disk import Disk
from linux.sysinfo import *
from linux import *
from setting import help_str
import time
import datetime


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


def show_bios_info():
	'''show server's bios info.'''
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type bios")
	print(dmi_info)


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
