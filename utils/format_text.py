#!/usr/bin/env python3
import re
import os
import sys
import subprocess


class Format_text(object):
	# create color function
	# dynamic function creation and also static function
	@staticmethod
	def color_dyn_function(code1, code2):
		def function_template(txt):
			# remove any style
			return str("\x1b[{};{}m{}\x1b[0m".format(code1,code2,re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))

		return function_template
		
	@staticmethod
	def emphasize_dyn_function(code):
		#tmp=""
		def function_template(txt):
			# remove any style
			return str("\x1b[{}m{}\x1b[0m".format(code,re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))

		return function_template
	
	@staticmethod
	def success(txt):
		# return str("  \x1b[1;32m \u221A\x1b[0m {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))
		return str(Format_text.lGreen("  \u221A")+" {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))

	@staticmethod
	def info(txt):
		# return str("  \x1b[0;36m#\x1b[0m {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))
		return str(Format_text.cyan("  #")+" {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))
	
	@staticmethod
	def error(txt):
		return str(Format_text.lRed("  \u00D7")+Format_text.red(" {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt))))
	
	@staticmethod
	def warning(txt):
		# return str("  \x1b[1;33m\u2206\x1b[0m {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))
		return str(Format_text.yellow("  \u2206")+" {}".format(re.sub("(\\x1b\[\d;\dm|\\x1b\[\dm)", "", txt)))

	@staticmethod
	def clear_screen():
		print("\x1b[2J")
		print("\x1b[H")
	
	@staticmethod
	def clear_scrolling_history():
		print("\x1b[2J\x1b[H\x1b[3J", end="")

	# the individual function are created here
	black=color_dyn_function.__func__(0,30)
	red=color_dyn_function.__func__(0,31)
	green=color_dyn_function.__func__(0,32)
	brown=color_dyn_function.__func__(0,33)
	blue=color_dyn_function.__func__(0,34)
	magenta=color_dyn_function.__func__(0,35)
	cyan=color_dyn_function.__func__(0,36)
	lGray=color_dyn_function.__func__(0,37)
	dGray=color_dyn_function.__func__(1,30)
	lRed=color_dyn_function.__func__(1,31)
	lGreen=color_dyn_function.__func__(1,32)
	yellow=color_dyn_function.__func__(1,33)
	lBlue=color_dyn_function.__func__(1,34)
	lMagenta=color_dyn_function.__func__(1,35)
	lCyan=color_dyn_function.__func__(1,36)
	white=color_dyn_function.__func__(1,37)
	
	bold=emphasize_dyn_function.__func__(1)
	uline=emphasize_dyn_function.__func__(4)
	iverse=emphasize_dyn_function.__func__(7)