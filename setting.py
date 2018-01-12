# coding = utf-8
from colorama import Fore
from prettytable import *


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

color = Colored()

log_path = "/root/server_info"
server_ip = "192.168.0.150"
server_logpath = "~/iads_log"
check_list = ["lsscsi", "sas2ircu", "sas3ircu", "storcli", "smartctl", "zpool", "zfs", "lsblk"]
t_row = PrettyTable()
t_row.hrules = ALL
t_row.vrules = ALL
t_row.field_names =[
	color.red("Command"),
	color.red("Help text")
]
t_row.align[color.red("Command")] = "l"
t_row.align[color.red("Help text")] = "l"
t_row.add_row(["iads show help", "Show this help menu."])
t_row.add_row(["iads show bios-info", "Show BIOS all info."])
t_row.add_row(["iads show bios-ver", "Show BIOS date version."])
t_row.add_row(["iads show bios-date", "Show BIOS date date."])
t_row.add_row(["iads show mem-model", "Show memory model."])
t_row.add_row(["iads show cpu-info", "Show CPU info."])
t_row.add_row(["iads show err-phy", "Show phys which have error."])
t_row.add_row(["iads show err-disk", "Show disks which have errors."])
t_row.add_row(["iads monitor gpu", "Monitor the temperature of GPUs and adjust the speed of the fan."])
t_row.add_row(["iads logging all", "Logging all the log."])
t_row.add_row(["iads logging upload", "Upload the log to server, only used in product line."])
t_row.add_row(["iads run linpack <minutes> \niads run paoyali <minutes>",
				"Run python linpack cpu and memory stress program,\nno param <minutes> means that always running. o_o"
])

help_str = ("iads 1.0.0\n"
			"iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg.\n"
			"Please makesure these tools are installed.\n\n"
			"help menu list:")
