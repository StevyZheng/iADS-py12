# coding = utf-8
from tmp.click_function_tmp import *


@click.group()
def main():
	pass


@click.command()
@click.option(
	'--show_err_phy',
	help="Show all the error phys info."
)
def show_err_phy():
	if not os.path.exists("/sys/class/sas_phy"):
		click.echo("System has no sas_phys.")
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
	click.echo(row)


@click.command()
@click.option(
	'--show_err_phy',
	help="Show all the error phys info."
)
def show_bios():
	if not os.path.exists("/usr/sbin/dmidecode"):
		print("dmidecode is not exists, please install dmidecode.")
		return
	dmi_info = exe_shell("dmidecode --type bios")
	print(dmi_info)


@click.option(
	'--show_err_disk',
	is_flag=True,
	callback=show_err_disk,
	expose_value=False,
	is_eager=True,
	help="Show all the error disk info, like smart info, fw, model or others."
)
@click.option(
	'--write_all_log',
	is_flag=True,
	callback=write_all_log,
	expose_value=False,
	is_eager=True,
	help="Write all the system info into json file which defind in setting file named log_path."
)
@click.option(
	'--show_bios',
	is_flag=True,
	callback=show_bios,
	expose_value=False,
	is_eager=True,
	help="Show system's bios info."
)
@click.option(
	'--monitor_gpu',
	is_flag=True,
	callback=gpu_monitor,
	expose_value=False,
	is_eager=True,
	help="Monitor all gpu temp."
)
def mains():
	require_str = "iads require smartctl, lsscsi, lsblk, sas3ircu, sas2ircu. Please makesure these tools are installed.";
	click.echo("=" * len(require_str))
	click.echo("\niads 1.0.0\n")
	click.echo(require_str)
	click.echo('\nInput iads --help to show help menu.\n')
	click.echo("=" * len(require_str))


main.add_command(show_err_phy)
main.add_command(show_bios)

if __name__ == '__main__':
	main()
