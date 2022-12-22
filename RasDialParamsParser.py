#!/usr/bin/env python3

# dru1d and stumblebot for executive office 2022!

import argparse

def ras_decode(string):
    output = bytes.fromhex(string).decode('utf-8')
    return output

def hex_list(string):
    hex_list = str.split(string, '000000')
    return hex_list

def null_count(string):
    count = str.count(string, '000000')
    return count

def file_search(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for entry in lines:
            # This was some half-assed attempt at pulling PSKs for L2TP VPN connections, but it failed miserably...
            # It was worth a shot! Credit to the original, probably better version of this idea goes to illwill.
            # if entry.find('L$_RasConnectionCredentials') == 0:
            #    count = null_count(entry)
            #    print(count)
            #    count = count+1
            #    if count % 9 == 0:
            #         num_connection = count +1 // 9
            #         for i in range(num_connection):
            #             hex = hex_list(str.split(entry,':')[1])
            #             if i == 0:
            #                 print (f'Preshared-Key{i}:  {ras_decode((hex[3][1:]))}')
            #                 i = i+1
            #             elif i > 0:
            #                 print (f'Preshared-Key{i}:  {ras_decode(hex[5])}')
            
            # This index is where the bytes for a username are located.
            index_user = 4
            # This index is where the bytes for a password are located.
            index_pass = 5
            hex = hex_list(str.split(entry,':')[1])

            if entry.find('RasDialParams') == 0:
                # there should be 8 fields delimited with \0x00\0x00\0x00 byte sequence
                # If we are able to determine the total number of fields and whether they're
                # divisible by 8, we can figure out how many times to loop through the bytes
                # to pull out creds. If an RadDialParam has less than 8 fields, which has been
                # obeserved occasionally, fall back to a single-parameter parser.
                count = null_count(entry)
                if count % 8 == 0:
                    num_connection = count // 8
                    for i in range(num_connection):
                        print (f'Username-{i}:\t {ras_decode(hex[index_user+8*i])}\nPassword-{i}:\t {ras_decode(hex[index_pass+8*i])}')
                else:
                    print (f'Username-0:\t {ras_decode(hex[index_user])}\nPassword-0:\t {ras_decode(hex[index_pass])}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Secretsdump *.secrets file with or other file with RasDialParams values', required=True)
    args = parser.parse_args()

    
    if args.file:
        hex = file_search(args.file)
    else:
        parser.print_help()
