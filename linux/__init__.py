# coding = utf-8
import traceback
import subprocess
import re


def try_catch(actual_do):
	def add_robust(*args, **keyargs):
		try:
			return actual_do(*args, **keyargs)
		except:
			print('Error execute: %s' % actual_do.__name__)
			# traceback.print_exc()
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
def search_regex_string(src_str, reg, split_str, column):
	if is_string_list([src_str, reg, split_str]):
		result = re.findall(reg, src_str)
		return result
	else:
		print("src_str is not string!")
		return None
