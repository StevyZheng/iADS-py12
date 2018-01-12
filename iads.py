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
	elif "help" == sw:
		show_help()
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
		show_bios_info()

monitor_parser = subparsers.add_parser("monitor")
monitor_parser_arg = monitor_parser.add_argument('monitor_name', nargs="*")
monitor_parser.set_defaults(func=monitor_func)


def logging_func(arg):
	sw = arg.logging_name[0]
	if "all" == sw:
		write_all_log()
	elif "upload" == sw:
		upload_logfile_to_server()

logging_parser = subparsers.add_parser("logging")
logging_parser_arg = logging_parser.add_argument('logging_name', nargs="*")
logging_parser.set_defaults(func=logging_func)


if __name__ == '__main__':
	args = parser.parse_args()
	args.func(args)
