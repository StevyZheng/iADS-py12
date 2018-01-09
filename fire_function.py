# coding = utf-8
from tmp.click_function_tmp import *


class Cli(object):
	def show_err_phy(self):
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
		print(row)

	def show_bios(self):
		if not os.path.exists("/usr/sbin/dmidecode"):
			print("dmidecode is not exists, please install dmidecode.")
			return
		dmi_info = exe_shell("dmidecode --type bios")
		print(dmi_info)

	def show_err_disk(self):
		err_disks_dict = Disk.get_err_disk_dict()
		err_disk_json = json.dumps(err_disks_dict, indent=1)
		print(err_disk_json)

	def write_all_log(self):
		log_dict = Log.get_all_log()
		phys_dict = Phy.phys_to_dict()
		controller_disk_dict = Controller.get_controllers_disks_all_dict()
		t_dict = {
			"sys_log": log_dict,
			"phys_log": phys_dict,
			"controller_disk_log": controller_disk_dict
		}
		if not os.path.exists(log_path):
			os.mkdir(log_path)

	def gpu_monitor(self):
		while True:
			Bmc.monitor_gpu_temp()
			time.sleep(4)
