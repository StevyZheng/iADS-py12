# coding = utf-8
from colorama import Fore

log_path = "/root/server_info"
server_ip = "192.168.0.150"
server_logpath = "~/iads_log"
check_list = ["lsscsi", "sas2ircu", "sas3ircu", "storcli", "smartctl", "zpool", "zfs", "lsblk"]
help_str = ("iads 1.0.0\n"
			"iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg.\n"
			"Please makesure these tools are installed.\n"
			"iads --> show --> help -- (Show this help menu.)\n"
			"              --> bios-info -- (Show BIOS all info.)\n"
			"              --> err-phy -- (Show phys which have error.)\n"
			"              --> err-disk -- (Show disks which have errors.)\n"
			"     --> monitor --> gpu -- (Monitor the temperature of GPUs and adjust the speed of the fan.)\n"
			"     --> logging --> all -- (Logging all the log.)\n"
			"     --> logging --> upload -- (Logging all the log.)\n")


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