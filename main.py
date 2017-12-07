# coding = utf-8
from linux.storage.phy import Phy
import linux
import time
import sys

i = 1
while True:
	print(Phy.err_phys_to_json())
	i += 1
	time.sleep(60)
