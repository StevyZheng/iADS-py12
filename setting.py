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
iads_help_list = (
	["iads show help", "Show this help menu."],
	["iads show bios-info", "Show BIOS all info."],
	["iads show bios-ver", "Show BIOS date version."],
	["iads show bios-date", "Show BIOS date date."],
	["iads show mem-model", "Show memory model."],
	["iads show cpu-info", "Show CPU info."],
	["iads show err-phy", "Show phys which have error."],
	["iads show err-disk", "Show disks which have errors."],
	["iads monitor gpu", "Monitor the temperature of GPUs and adjust the speed of the fan."],
	["iads logging all", "Logging all the logs."],
	["iads logging print-err", "Print err logs."],
	["iads logging upload", "Upload the log to server, only used in product line."],
	["iads run linpack <minutes> \niads run paoyali <minutes>",
		"Run python linpack cpu and memory stress program,\nno param <minutes> means that always running. o_o"],
	["iads run reboot <sec>", "Run the reboot interval <sec>."],
	["iads run reboot clean", "Clean all the reboot log."],
	["iads run reboot rm", "rm all reboot files."],
)
for line in iads_help_list:
	t_row.add_row(line)

help_str = ("iads 1.0.0\n"
			"iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg, pkill.\n"
			"Please makesure these tools are installed.\n\n"
			"help menu list:")

