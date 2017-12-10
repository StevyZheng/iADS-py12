# coding = utf-8
from setting import *
from prettytable import *
import click
import json
import os
from linux.storage.phy import Phy
from linux.storage.disk import DiskFromLsiSas3, DiskFromLsiSas2
from linux.storage.controller import Controller, LsiSas3Controller, LsiSas2Controller


def show_err_phy(ctx, param, value):
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
	if not value or ctx.resilient_parsing:
		return
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
	click.echo(row)
	ctx.exit()


def show_err_disk(ctx, param, value):
	if not value or ctx.resilient_parsing:
		return
	cons = Controller.get_controllers_disks_all_dict()
	ctx.exit()


def log_all_info(ctx, param, value):
	phys_dict = Phy.phys_to_dict()
	phy_json = json.dumps(phys_dict, indent=1)
	controller_disk_dict = Controller.get_controllers_disks_all_dict()
	controller_disk_json = json.dumps(controller_disk_dict, indent=1)
	with open((os.path.join(log_path, "phy.json")), 'w') as json_file:
		json_file.write(phy_json)
		json_file.write(controller_disk_json)
	return
