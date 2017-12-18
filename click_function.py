# coding = utf-8
from setting import *
from prettytable import *
import click
import json
import os
from linux import try_catch
from linux.storage.phy import Phy
from linux.storage.disk import DiskFromLsiSas3, DiskFromLsiSas2, Disk
from linux.storage.controller import Controller, LsiSas3Controller, LsiSas2Controller


@try_catch
def write_json_file(file_name, t_dict):
	t_json = json.dumps(t_dict, indent=1)
	with open((os.path.join(log_path, file_name)), 'w') as json_file:
		json_file.write(t_json)


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
	err_disks_dict = Disk.get_err_disk_dict()
	err_disk_json = json.dumps(err_disks_dict, indent=1)
	click.echo(err_disk_json)
	ctx.exit()


@try_catch
def log_all_info(ctx, value):
	if not value or ctx.resilient_parsing:
		return
	phys_dict = Phy.phys_to_dict()
	controller_disk_dict = Controller.get_controllers_disks_all_dict()
	if not os.path.exists(log_path):
		os.mkdir(log_path)
	write_json_file(os.path.join(log_path, "phy_info.json"), phys_dict)
	write_json_file(os.path.join(log_path, "disk_info.json"), controller_disk_dict)
	ctx.exit()

