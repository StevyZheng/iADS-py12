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
	'--check_env',
	default='help',
	help="Check env."
)
def main(check_env):
	click.echo('Options:\n  --%s  Show help menu.' % check_env)

if __name__ == '__main__':
	main()
