# coding = utf-8
import os

from colorama import init, Fore, Back, Style
from prettytable import *
import json
from linux import try_catch, exe_shell
from linux.storage.controller import Controller
from linux.storage.disk import Disk
from linux.storage.phy import Phy
import time
from linux.sysinfo import *


class Colored(object):
	def yellow(self, s):
		return Fore.LIGHTYELLOW_EX + s + Fore.RESET

	def white(self, s):
		return Fore.LIGHTWHITE_EX + s + Fore.RESET

	def red(self, s):
		return Fore.LIGHTRED_EX + s + Fore.RESET

	def green(self, s):
		return Fore.LIGHTGREEN_EX + s + Fore.RESET

	def blue(self, s):
		return Fore.LIGHTBLUE_EX + s + Fore.RESET


class Cli(object):
	def __init__(self, log_path="~/iads_log"):
		self.log_path = log_path

	def help(self):
		color = Colored()
		help_dict = {
			"help": "Show this help menu.",
			"show-err-phy": "Show error phys in a list.",
			"show-err-disk": "Show error disk in a dict.",
			"show-bios": "Show server's BIOS info.",
			"write-all-log --log-path=<path>": "Write all logs into <path>.",
			"gpu-monitor": "Monitor GPU's Temp."
		}
		row = PrettyTable()
		row.hrules = ALL
		row.vrules = ALL
		row.field_names = [color.red("param"), color.red("help_str"), ]
		row.align[color.red("param")] = "l"
		row.align[color.red("help_str")] = "l"
		for (key, value) in help_dict.items():
			row.add_row([key, value])
		help_str = "%s\n%s\n%s\n%s" % (
			"iads 1.0.0",
			color.blue("iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg." \
				" Please makesure these tools are installed."),
			"Input \"iads help\" to show help menu.",
			row
		)
		print(help_str)

	def show_err_phy(self):
		if not os.path.exists("/sys/class/sas_phy"):
			print("System has no sas_phys.")
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

	def show_bios(self):
		'''show server's bios info.'''
		if not os.path.exists("/usr/sbin/dmidecode"):
			print("dmidecode is not exists, please install dmidecode.")
			return
		dmi_info = exe_shell("dmidecode --type bios")
		print(dmi_info)

	def show_err_disk(self):
		err_disks_dict = Disk.get_err_disk_dict()
		err_disk_json = json.dumps(err_disks_dict, indent=1)
		print(err_disk_json)

	def write_all_log(self):
		log_dict = Log.get_all_log()
		phys_dict = Phy.phys_to_dict()
		controller_disk_dict = Controller.get_controllers_disks_all_dict()
		t_dict = {
			"sys_log": log_dict,
			"phys_log": phys_dict,
			"controller_disk_log": controller_disk_dict
		}
		if not os.path.exists(log_path):
			os.mkdir(log_path)

	def gpu_monitor(self):
		while True:
			Bmc.monitor_gpu_temp()
			time.sleep(4)
