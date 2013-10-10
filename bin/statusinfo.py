#!/usr/bin/env python
# Simple python systeminfo status script built for i3
# requirements:
#   psutil
#   sh

import sys
import json
import time
import psutil
# import sh

UPDATE_INTERVAL = 1
RED = "#803232"
GREEN = "#005500" #89b83f
BLUE = "#324c80"
newsbeuter = sh.Command("/usr/bin/newsbeuter")
newsbeuter = newsbeuter.bake(x="print-unread")


class Formatter(object):
	def __init__(self):
		pass

	def __call__(self, function):
		def wrapper(*args, **kwargs):
			text, color = function(*args)
			return {"full_text": " {0} ".format(text), "color": color}
		return wrapper

@Formatter()
def currtime():
	return (time.strftime("%H:%M:%S"), GREEN)

@Formatter()
def currdate():
	return (time.strftime("%m/%d/%Y"), GREEN)

@Formatter()
def cpuinfo():
	percent = psutil.cpu_percent()
	if percent >= 90:
		return ("CPU: {0}".format(percent), RED)
	elif percent <= 10:
		return ("CPU: {0}".format(percent), BLUE)
	else:
		return ("CPU: {0}".format(percent), GREEN)

@Formatter()
def meminfo():
	mem = int((psutil.virtual_memory().active/psutil.virtual_memory().total)*100)
	if mem >= 90:
		return ("MEM: {0}%".format(mem), RED)
	elif mem <= 10:
		return ("MEM: {0}%".format(mem), BLUE)
	else:
		return ("MEM: {0}%".format(mem), GREEN)

@Formatter()
def diskinfo(disk, name):
	disk = psutil.disk_usage(disk)
	used = int(disk.used/1073741824)
	total = int(disk.total/1073741824)
	percent = int(disk.percent)
	if percent >= 80:
		return ("{0} {1}/{2}GB ({3}% USED)".format(name, used, total, percent), RED)
	elif percent <= 10:
		return ("{0} {1}/{2}GB ({3}% USED)".format(name, used, total, percent), BLUE)
	else:
		return ("{0} {1}/{2}GB ({3}% USED)".format(name, used, total, percent), GREEN)

@Formatter()
def news():
	n = newsbeuter().strip()
	return (n if n else "newsbeuter open", RED)

if __name__ == "__main__":
	print("{ \"version\": 1 }")
	sys.stdout.flush()
	print("[")
	sys.stdout.flush()
	print("[],")
	sys.stdout.flush()

	while True:
		info = []
		info.append(currtime())
		info.append(currdate())
		info.append(cpuinfo())
		info.append(meminfo())
		info.append(diskinfo("/", "root"))
		info.append(diskinfo("/home", "Home"))
		info.append(diskinfo("/mnt/share", "NAS"))
		info.append(news())

		print(json.dumps(info)+",")
		sys.stdout.flush()
		time.sleep(UPDATE_INTERVAL)

