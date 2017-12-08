# coding = utf-8
import click
import linux
from prettytable import *
from linux.storage.phy import Phy
from linux.storage.disk import DiskFromLsiSas3, DiskFromLsiSas2
from linux.storage.controller import LsiSas3Controller, LsiSas2Controller


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
	ctx.exit()


@click.command()
@click.option(
	'--show_err_phy',
	is_flag=True,
	callback=show_err_phy,
	expose_value=False,
	is_eager=True,
	help="Show all the error phys info."
)
def main(count, name):
	for x in range(count):
		click.echo('Hello %s!' % name)

if __name__ == '__main__':
	main()
