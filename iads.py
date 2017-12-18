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
	help="write all the system info into json file which defind in setting file named log_path."
)
@click.option(
	'--write_log',
	is_flag=True,
	callback=log_all_info,
	expose_value=False,
	is_eager=True,
	help="write all the system info into json file which defind in setting file named log_path."
)
def main():
	click.echo('')

if __name__ == '__main__':
	main()
