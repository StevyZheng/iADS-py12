# coding = utf-8

log_path = "/root/server_info"
check_list = ["lsscsi", "sas2ircu", "sas3ircu", "storcli", "smartctl", "zpool", "zfs", "lsblk"]
help_str = ("iads 1.0.0\n"
			"iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg.\n"
			"Please makesure these tools are installed."
			"iads --> help -- Show this help menu.\n"
			"     --> show --> bios-info -- Show BIOS all info.\n"
			"              --> err-phy -- Show phys which have error.\n"
			"              --> err-disk -- Show disks which have errors.\n")
