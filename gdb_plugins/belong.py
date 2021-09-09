from __future__ import print_function

import gdb
import os

class Belong(gdb.Command):
	def __init__(self):
		super(Belong, self).__init__("belong", gdb.COMMAND_USER)

	def invoke(self, args, from_tty):
		arg = args.split(" ")[0]
		
		if len(arg) == 0:
			print("belong <address>")
			return

		addr = gdb.parse_and_eval(arg)
		pid = gdb.selected_inferior().pid

		with open("/proc/{}/maps".format(pid), "r") as f:
			maps = f.readlines()

		# find mapping
		for v in maps:
			start, end = v.split(' ')[0].split('-')

			start = int(start, 16)
			end = int(end, 16)

			if (start <= addr < end):
				print(v, end="")
				return
		print("no mapping found for address")


class Belongc(gdb.Command):
	def __init__(self):
		super(Belongc, self).__init__("belongc", gdb.COMMAND_USER)

	def nice_msg(self, text, color, attr):
		COLORS = {"black": "30", "red": "31", "green": "32", "yellow": "33",
					"blue": "34", "purple": "35", "cyan": "36", "white": "37"}
		CATTRS = {"regular": "0", "bold": "1", "underline": "4", "strike": "9",
					"light": "1", "dark": "2", "invert": "7"}

		return "\033[;" + CATTRS[attr] + ";" + COLORS[color] + "m" + text + "\033[0m"

	def invoke(self, args, from_tty):
		arg = args.split(" ")[0]
		if len(arg) == 0:
			print("belongc <address>")
			return

		addr = gdb.parse_and_eval(arg)
		pid = gdb.selected_inferior().pid

		with open("/proc/{}/maps".format(pid), "r") as f:
			maps = f.readlines()

		found = False

		buf = ""

		# find mapping
		for v in maps:
			if found:
				buf += v
				continue

			start, end = v.split(' ')[0].split('-')

			start = int(start, 16)
			end = int(end, 16)

			# found mapping
			if (start <= addr < end):
				found = True
				buf += self.nice_msg(v, "cyan", "bold")
			else:
				buf += v

		if not found:
			print("no mapping found for address")
		else:
			print(buf)


# load the commands
Belong()
Belongc()