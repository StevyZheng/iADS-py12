# coding = utf-8
from linux import try_catch
import linux
import json


class Phy:
	def __init__(self, t_phy_name):
		self.phy_name = t_phy_name
		self.invalid_dword_count = ""
		self.loss_of_dword_sync_count = ""
		self.phy_reset_problem_count = ""
		self.running_disparity_error_count = ""
		self.sas_address = ""
	
	@try_catch
	def fill_attrs(self):
		invalid_dword_count_path = "/sys/class/sas_phy/%s/invalid_dword_count" % self.phy_name
		loss_of_dword_sync_count_path = "/sys/class/sas_phy/%s/loss_of_dword_sync_count" % self.phy_name
		phy_reset_problem_count_path = "/sys/class/sas_phy/%s/phy_reset_problem_count" % self.phy_name
		running_disparity_error_count_path = "/sys/class/sas_phy/%s/running_disparity_error_count" % self.phy_name
		sas_address_path = "/sys/class/sas_phy/%s/sas_address" % self.phy_name
		self.invalid_dword_count = linux.read_file(invalid_dword_count_path).strip()
		self.loss_of_dword_sync_count = linux.read_file(loss_of_dword_sync_count_path).strip()
		self.phy_reset_problem_count = linux.read_file(phy_reset_problem_count_path).strip()
		self.running_disparity_error_count = linux.read_file(running_disparity_error_count_path).strip()
		self.sas_address = linux.read_file(sas_address_path).strip()
	
	@staticmethod
	@try_catch
	def scan_phys():
		return linux.list_dir_all_files("/sys/class/sas_phy")
	
	@staticmethod
	@try_catch
	def scan_phys_attr():
		phy_arr = []
		for phy in Phy.scan_phys():
			p = Phy(phy)
			p.fill_attrs()
			phy_arr.append(p)
		return phy_arr
	
	@staticmethod
	@try_catch
	def scan_err_phys():
		phy_arr = []
		for phy in Phy.scan_phys():
			p = Phy(phy)
			p.fill_attrs()
			if int(p.invalid_dword_count) > 0 or int(p.loss_of_dword_sync_count) > 0 or int(
					p.phy_reset_problem_count) > 0 or int(p.running_disparity_error_count) > 0:
				phy_arr.append(p)
		return phy_arr

	@staticmethod
	@try_catch
	def phys_to_dict():
		phy_arr = Phy.scan_phys_attr()
		phys_dict = {}
		for p in phy_arr:
			phy_dict = {
				"phy_name": p.phy_name,
				"sas_address": p.sas_address,
				"invalid_dword_count": p.invalid_dword_count,
				"loss_of_dword_sync_count": p.loss_of_dword_sync_count,
				"phy_reset_problem_count": p.phy_reset_problem_count,
				"running_disparity_error_count": p.running_disparity_error_count
			}
			phys_dict[p.phy_name] = phy_dict
		return phys_dict

	@staticmethod
	@try_catch
	def err_phys_to_dict():
		phy_arr = Phy.scan_err_phys()
		phys_dict = {}
		for p in phy_arr:
			phy_dict = {
				"phy_name": p.phy_name,
				"sas_address": p.sas_address,
				"invalid_dword_count": p.invalid_dword_count,
				"loss_of_dword_sync_count": p.loss_of_dword_sync_count,
				"phy_reset_problem_count": p.phy_reset_problem_count,
				"running_disparity_error_count": p.running_disparity_error_count
			}
			phys_dict[p.phy_name] = phy_dict
		return phys_dict

	@staticmethod
	@try_catch
	def phys_to_json():
		phys_dict = Phy.phys_to_dict()
		phy_json = json.dumps(phys_dict, indent=1)
		return phy_json

	@staticmethod
	@try_catch
	def err_phys_to_json():
		err_phys_dict = Phy.err_phys_to_dict()
		phy_json = json.dumps(err_phys_dict, indent=1)
		return phy_json
