# coding = utf-8
from click_function import *


@click.command()
@click.option(
	'--show_err_phy',
	is_flag=True,
	callback=show_err_phy,
	expose_value=False,
	is_eager=True,
	help="Show all the error phys info."
)
@click.option(
	'--show_err_disk',
	is_flag=True,
	callback=show_err_disk,
	expose_value=False,
	is_eager=True,
	help="Show all the error disk info, like smart info, fw, model or others."
)
@click.option(
	'--write_log',
	is_flag=True,
	callback=log_all_info,
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
def main():
	require_str = "iads require smartctl, lsscsi, lsblk, sas3ircu, sas2ircu. Please makesure these tools are installed.";
	click.echo("=" * len(require_str))
	click.echo("\niads 1.0.0\n")
	click.echo(require_str)
	click.echo('\nInput iads --help to show help menu.\n')
	click.echo("=" * len(require_str))

if __name__ == '__main__':
	main()
