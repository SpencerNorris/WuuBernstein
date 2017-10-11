#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
Description: Script for Wuu-Bernstein client.
'''

import sys


def client():
	#Command functions
	__tweet():
		pass

	__show():
		pass

	__block():
		pass

	__unblock():
		pass


	VALID_COMMANDS = ['view', 'tweet', 'block', 'unblock', 'exit']
	while(1):
		input_var = input("Enter a command: ").lower()
		if not input_var in VALID_COMMANDS:
			print("Invalid command!\n")
			continue
		elif input_var == 'exit':
			break
		else:
			{
				'tweet': __tweet,
				'show': __show,
				'block': __block,
				'unblock': __unblock
			}[input_var]()
		return 0

if __name__ == '__main__':
	sys.exit(client())