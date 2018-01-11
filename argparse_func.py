# coding = utf-8
from linux import *
from prettytable import *
from linux.storage.controller import Controller
from linux.storage.disk import Disk
from linux.storage.phy import Phy
import time, os
from linux.sys import *


def iads_help():
	param_dict = json_to_dict(os.path.join(get_main_path(), "param.json"))
	print(param_dict)


def show_help():
	help_str = (
		"=" * 80,
		"iads show",
		"help  -->  Show this menu.",
		"bios-info  -->  Show all BIOS info.",
		"=" * 80
	)
	s = ""
	for line in help_str:
		s = "%s\n%s" % (s, line)


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
