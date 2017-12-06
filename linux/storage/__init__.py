# coding = utf-8
import linux


def scan_controller():
	sas2_con = linux.exe_shell("sas2ircu list|grep -P 'SAS[0-9]{4}'")
	sas3_con = linux.exe_shell("sas3ircu list|grep -P 'SAS[0-9]{4}'")
	mega_raid_con = linux.exe_shell("storcli show|grep LSI")
	if "" == sas2_con.strip():
		indexs = linux.search_regex_strings_column(sas2_con, ".*SAS[0-9]{4}.*", " ", 0)
		con_str = linux.search_regex_strings(sas2_con, "SAS[0-9]{4}")


def scan_from_sas23_disk_name_sn():
	disks = []
	tmp = linux.exe_shell("lsblk -o NAME,SERIAL,VENDOR")
	names = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +([a-z]|[A-Z]|[0-9]| )+", " ", 0)
	sns = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +([a-z]|[A-Z]|[0-9]| )+", " ", 1)
	vendors = linux.search_regex_strings_column(tmp, "^sd[a-z]+ +([a-z]|[A-Z]|[0-9]| )+", " ", 2)
	for i, e in enumerate(names):
		attr = [
			names[i],
			sns[i],
			vendors[i],
		]
		disks.append(attr)
	return disks