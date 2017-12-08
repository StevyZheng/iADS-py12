# coding = utf-8
import linux


class Zfs:
	def __init__(self):
		self.disks = None

	@staticmethod
	def install_zfs():
		linux.zfs_install()

	def set_zfs_disks(self, disk_list):
		counts = len(disk_list)
		if counts > 3 and counts % 2 == 0:
			self.disks = disk_list
		else:
			raise Exception("disk_list len is not even number!")

	def create_pool(self, pool_name, pool_level):
		zpool_str = "zpool create %s raidz" % pool_name
		if "raidz-2" in pool_name:
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
