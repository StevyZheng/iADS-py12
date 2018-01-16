# coding = utf-8
import linux
from linux.storage.controller import Controller


class Zfs:
	def __init__(self):
		self.disks = []

	def scan_fill_disks(self):
		dict_disks = Controller.get_controllers_disks_all_dict()
		tmp_disk_list = []
		for index in dict_disks.iterkeys():
			for k in dict_disks[index].iterkey():
				tmp_disk_list.append(k)
		disk_list_size = len(tmp_disk_list)
		if disk_list_size > 2:
			self.disks = tmp_disk_list
		else:
			print("Please make disks more than 2.")
			raise Exception("Disks are least then 2! Please add disk.")

	def init_disk(self):
		for i in self.disks:
			linux.exe_shell("dd if=/dev/zero of=/dev/%s bs=1M count=100" % i)
			linux.exe_shell("parted /dev/%s -s mklabel gpt" % i)

	def set_zfs_disks(self, disk_list):
		counts = len(disk_list)
		if counts > 3 and counts % 2 == 0:
			self.disks = disk_list
		else:
			raise Exception("disk_list len is not even number!")

	def create_pool(self, pool_name, pool_level):
		if not linux.bin_exists("zpool"):
			print("zpool is not exists!")
			return
		zpool_str = "zpool create %s raidz" % pool_name
		if "raidz-2" == pool_level:
			if len(self.disks) < 6:
				raise Exception("raidz-2 request more than 6 disks!")
			for i in self.disks[:len(self.disks)/2]:
				zpool_str = "%s %s" % (zpool_str, i)
			zpool_str = "%s raidz" % zpool_str
			for i in self.disks[len(self.disks)/2+1:]:
				zpool_str = "%s %s" % (zpool_str, i)
			return linux.exe_shell(zpool_str)

	def destroy_pool(self, pool_name):
		zpool_str = "zpool destroy %s" % pool_name
		result = linux.exe_shell(zpool_str)
		if '' == result:
			for i in self.disks:
				linux.exe_shell("dd if=/dev/zero of=/dev/%s bs=1M count=100 >> /dev/null" % i)
		return result
