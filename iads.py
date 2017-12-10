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
	'--write_log',
	is_flag=True,
	callback=log_all_info,
	expose_value=False,
	is_eager=True,
	help="write all the system info into json file which defind in setting file named log_path"
)
def main(count, name):
	for x in range(count):
		click.echo('Hello %s!' % name)

if __name__ == '__main__':
	main()
