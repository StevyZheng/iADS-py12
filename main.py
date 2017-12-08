# coding = utf-8
from linux.storage.disk import DiskFromLsiSas3
from linux.storage.controller import LsiSas3Controller
import linux
import time
import sys


cons = LsiSas3Controller.scan_controller()
for i in cons:
	print(i.model)