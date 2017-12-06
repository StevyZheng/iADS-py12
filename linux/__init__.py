# coding = utf-8
import traceback
import subprocess
import re
import os


def try_catch(actual_do):
	def add_robust(*args, **keyargs):
		try:
			return actual_do(*args, **keyargs)
		except:
			print('Error execute: %s' % actual_do.__name__)
			traceback.print_exc()
		return add_robust


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
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	a = p.stdout.read()
	return a


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
		result = re.findall(reg, src_str)
		re_list = []
		for line in result:
			list_re = line.split(split_str)
			re_list.append(list_re[column])
		return result
	else:
		print("src_str is not string!")
		return None


@try_catch
def get_match_sub_string(src_str, reg_str):
	if is_string_list([src_str, reg_str]):
		return re.search(reg_str, src_str).group(0)


@try_catch
def read_file(path):
	with open(path) as f:
		return f.read()


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
