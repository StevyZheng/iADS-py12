# coding = utf-8
from linux.storage.disk.disk import DiskFromLsiSas3
import linux

disk = DiskFromLsiSas3("K7GJ27UL", "sdb")
disk.fill_attrs()
print(disk.to_json())

