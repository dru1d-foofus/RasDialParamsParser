#!/usr/bin/env python3

# dru1d and stumblebot for executive office 2022!

import argparse

def ras_decode(string):
	output = bytes.fromhex(string).decode('utf-8')
	return output

def hex_list(string):
	hex_list = str.split(string, '000000')
	return hex_list

def file_search(filename):
	with open(filename, 'r') as file:
		lines = file.readlines()
		for entry in lines:
			if entry.find('RasDialParams') == 0:
				hex = hex_list(str.split(entry,':')[1])
				print(f'Username: {ras_decode(hex[4])} Password: {ras_decode(hex[5])}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', help='Raw hex string', required=False)
    parser.add_argument('-f', '--file', help='Secretsdump *.secrets file with or other file with RasDialParams values', required=False)
    args = parser.parse_args()

    if args.string:
    	hex = hex_list(args.string)
    	print(f'Username: {ras_decode(hex[4])} Password: {ras_decode(hex[5])}')
    elif args.file:
    	hex = file_search(args.file)
    else:
    	parser.print_help()
