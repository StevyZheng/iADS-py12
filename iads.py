# coding = utf-8
import argparse
from argparse_func import *


def iads_func(arg):
	sw = arg.help[0]
	if "help" == sw:
		show_help()


parser = argparse.ArgumentParser(
	prog="iads",
	usage="%(prog)s [options]",
	description="iads 1.0.0, cli tool for roycom." \
	" iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg." \
	" Please makesure these tools are installed.",
)
subparsers = parser.add_subparsers(help="iads params")


def show_func(arg):
	sw = arg.show_name[0]
	if "bios-info" == sw:
		show_bios_info()
	elif "bios-ver" == sw:
		show_bios_ver()
	elif "bios-date" == sw:
		show_bios_date()
	elif "cpu-info" == sw:
		show_cpu_info()
	elif "help" == sw:
		show_help()
	elif "mem-model" == sw:
		show_mem_model()
	elif "err-phy" == sw:
		show_err_phy()
	elif "err-disk" == sw:
		show_err_disk()

show_parser = subparsers.add_parser("show")
show_parser_arg = show_parser.add_argument('show_name', nargs="*")
show_parser.set_defaults(func=show_func)


def monitor_func(arg):
	sw = arg.monitor_name[0]
	if "gpu" == sw:
		gpu_monitor()
	elif "log" == sw:
		log_monitor()

monitor_parser = subparsers.add_parser("monitor")
monitor_parser_arg = monitor_parser.add_argument('monitor_name', nargs="*")
monitor_parser.set_defaults(func=monitor_func)


def logging_func(arg):
	sw = arg.logging_name[0]
	if "all" == sw:
		write_all_log()
	elif "print-err" == sw:
		print_err_log()
	elif "upload" == sw:
		upload_logfile_to_server()

logging_parser = subparsers.add_parser("logging")
logging_parser_arg = logging_parser.add_argument('logging_name', nargs="*")
logging_parser.set_defaults(func=logging_func)


def run_func(arg):
	sw = arg.run_name[0]
	if "linpack" == sw or "paoyali" == sw:
		if len(arg.run_name) > 1 and arg.run_name[1]:
			run_time = arg.run_name[1]
		else:
			run_time = -1
		run_linpack(run_time)
	elif "reboot" == sw:
		if len(arg.run_name) > 1 and arg.run_name[1]:
			run_sec = arg.run_name[1]
			if str(run_sec).isdigit():
				run_reboot(run_sec)
			elif run_sec == "clean":
				clean_reboot()
			elif run_sec == "rm":
				rm_reboot()


run_parser = subparsers.add_parser("run")
run_parser_arg = run_parser.add_argument('run_name', nargs="*")
run_parser.set_defaults(func=run_func)


if __name__ == '__main__':
	args = parser.parse_args()
	args.func(args)
