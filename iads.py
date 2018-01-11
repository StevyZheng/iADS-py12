# coding = utf-8
import argparse
from argparse_func import *


parser = argparse.ArgumentParser(
	prog="iads",
	usage="%(prog)s [options]",
	description="iads 1.0.0, cli tool for roycom." \
	" iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg." \
	" Please makesure these tools are installed.",
)


def show_func(arg):
	sw = arg.show_name[0]
	print(sw)
	if "bios-info" == sw:
		show_bios_info()
	elif "help" == sw:
		show_help()
	elif "err-phy" == sw:
		show_err_phy()

subparsers = parser.add_subparsers(help="Show info")
show_parser = subparsers.add_parser("show")
show_parser_arg = show_parser.add_argument('show_name', nargs="*", help="1231212\n536")
show_parser.set_defaults(func=show_func)


if __name__ == '__main__':
	args = parser.parse_args()
	args.func(args)
