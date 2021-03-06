# coding = utf-8
import traceback
import subprocess
import re
import os
import sys
import shutil
import stat
import json
from setting import *


def try_catch(f):
	def handle_problems(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except Exception:
			exc_type, exc_instance, exc_traceback = sys.exc_info()
			formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
			message = '\n{0}\n{1}:\n{2}'.format(
				formatted_traceback,
				exc_type.__name__,
				exc_instance
			)
			# raise exc_type(message)
			print(exc_type(message))
		finally:
			pass

	return handle_problems


def dict_to_json(t_dict):
	str_json = json.dumps(t_dict, indent=1)
	return str_json


def json_to_dict(json_file):
	str_t = read_file(json_file)
	return json.loads(str_t)


def dict_to_json_file(t_dict, file_path):
	with open(file_path, 'w') as f:
		json.dump(t_dict, f)


def is_string(s):
	return isinstance(s, str)


def is_string_list(s):
	if isinstance(s, list):
		for i in s:
			if not is_string(i):
				return False
		return True
	else:
		return False


@try_catch
def exe_shell(cmd):
	pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	pro = pro.communicate()
	if (pro[1] is None) and (pro[0] is not None):
		return pro[0]
	elif (pro[1] is not None) and (pro[0] is None):
		return pro[1]
	elif (pro[1] is not None) and (pro[0] is not None):
		return "%s\n%s" % (pro[0], pro[1])
	else:
		return None


@try_catch
def search_regex_strings(src_str, reg):
	if is_string_list([src_str, reg]):
		result = re.findall(reg, src_str)
		return result
	else:
		print("src_str is not string!")
		return None


@try_catch
def search_regex_strings_column(src_str, reg, split_str, column):
	if is_string_list([src_str, reg, split_str]):
		result = re.findall(reg, src_str, re.M)
		re_list = []
		for line in result:
			list_re = line.split(split_str)
			re_list.append(list_re[column].strip())
		return re_list
	else:
		print("src_str is not string!")
		return None


@try_catch
def search_regex_one_line_string_column(src_str, reg, split_str, column):
	if is_string_list([src_str, reg, split_str]):
		result = re.findall(reg, src_str, re.M)
		if result:
			list_re = result[0].split(split_str)
			return list_re[column].strip()
		else:
			return None
	else:
		print("src_str is not string!")
		return None


@try_catch
def get_match_sub_string(src_str, reg_str):
	if is_string_list([src_str, reg_str]):
		return re.search(reg_str, src_str).group(0)


def read_file(file_path):
	if os.path.exists(file_path) and os.path.isfile(file_path):
		with open(file_path) as fp:
			try:
				s_t = fp.read()
			except Exception:
				return "-9999"
	else:
		print("file not exists or path is not a file!")
		return "-9999"
	return s_t


def write_file(file_path, buf):
	if os.path.exists(file_path) and os.path.isfile(file_path):
		with open(file_path) as fp:
			try:
				fp.write(buf)
			except Exception:
				return "-9999"
	else:
		print("file not exists or path is not a file!")
		return "-9999"


@try_catch
def list_dir_all_files(path):
	return os.listdir(path)


@try_catch
def list_dir_normal_files(path):
	files = os.listdir(path)
	result = []
	for i in files:
		file_path = os.path.join(path, i)
		if os.path.isfile(file_path):
			result.append(i)
	return result


def path_join(path1, path2):
	return os.path.join(path1, path2)


def get_main_path():
	dir_name, file_name = os.path.split(os.path.abspath(sys.argv[0]))
	return dir_name


def bin_exists(bin_name):
	re = exe_shell(bin_name)
	if "-bash:" in re:
		return False
	else:
		return True


def check_unexists_tools():
	unexists_list = []
	for i in check_list:
		if not bin_exists(i):
			unexists_list.append(i)
	return unexists_list


@try_catch
def copy_tools():
	exes = ["sas2ircu", "sas3ircu", "storcli", ]
	main_path = get_main_path()
	for i in exes:
		shutil.copyfile(os.path.join(main_path, "tools/%s" % i), os.path.join("/bin", i))
		os.chmod("/bin/%s" % i, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)


@try_catch
def rm_tools():
	exes = ["sas2ircu", "sas3ircu", "storcli", ]
	for i in exes:
		file_path = os.path.join("/bin", i)
		if os.path.exists(file_path):
			os.remove(file_path)


@try_catch
def zfs_install():
	return exe_shell("cd %s/tools && ./install_zfs.sh" % get_main_path())


@try_catch
def reboot(sec):
	if sec < 15:
		print("Reboot sec is too short! Please large than 15.")
	file_path = "/usr/local/reboot.sh"
	reboot_count = "/var/log/reboot.count"
	reboot_log = "/var/log/reboot.log"
	exe_shell("echo 0 > %s" % reboot_count)
	reboot_str_list = (
		"#!/bin/sh\n",
		"date_t=`date`\n",
		"count_path=\"/var/log/reboot.count\"\n",
		"log_path=\"/var/log/reboot.log\"\n",
		"count=`cat $count_path`\n",
		"echo \"reboot times: $count, date: $date_t\" >> $log_path\n",
		"let count=count+1\n",
		"echo $count > $count_path\n",
		"sleep %s\n" % sec,
		"reboot\n"
	)
	with open(reboot_log, "w") as fp:
		fp.writelines(reboot_str_list)
	exe_shell("chmod 777 %s && chmod +x /etc/rc.local" % file_path)
	if not os.path.exists(file_path):
		exe_shell("echo \"nohup /usr/local/reboot.sh &\" >> /etc/rc.local")


@try_catch
def un_reboot():
	exe_shell("pkill reboot.sh")


@try_catch
def rm_reboot_t():
	file_path = "/usr/local/reboot.sh"
	if not os.path.exists(file_path):
		os.remove(file_path)
	exe_shell("sed -i '/nohup/'d /etc/rc.local")


@try_catch
def clean_reboot_log():
	reboot_count = "/var/log/reboot.count"
	reboot_log = "/var/log/reboot.log"
	exe_shell("echo 0 > %s && echo \"\" > %s" % (reboot_count, reboot_log))


@try_catch
def pretty_dict(o_dict, o_indent=' '):
	def _pretty(i_dict, i_indent):
		for i, tup in enumerate(i_dict.items()):
			k, v = tup
			if isinstance(k, str):
				k = '"%s"' % k
			if isinstance(v, str):
				v = '"%s"' % v
			if isinstance(v, dict):
				v = ''.join(_pretty(v, i_indent + ' ' * len(str(k) + ': {')))
			if i == 0:
				if len(i_dict) == 1:
					yield '{%s: %s}' % (k, v)
				else:
					yield '{%s: %s,\n' % (k, v)
			elif i == len(i_dict) - 1:
				yield '%s%s: %s}' % (i_indent, k, v)
			else:
				yield '%s%s: %s,\n' % (i_indent, k, v)
	return ''.join(_pretty(o_dict, o_indent))
