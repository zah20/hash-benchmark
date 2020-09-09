#!/usr/bin/python3
import sys, subprocess, os, time

##################################################
# Program:       Hashbenchmark.py
# License:       GPLv3
# Version:       0.1
# Author:        zah20
#
# Last Modified: Wed Sep 09, 2020 (07:30 PM)
#
# For crc32 hash checks, please install crctk 
# Source: https://github.com/2ion/crctk
##################################################


##################################################
#               Global Variables
##################################################
global file_list, openssl_hash_types, openssl_path, \
    crctk_path, skip_crc32, data

# Modify this if you have different files
file_list = ['2GB', '4GB', '6GB']

openssl_hash_types = ['-md5', '-sha1', '-sha224', '-sha3-256', \
        '-sha-256', '-ripemd', '-whirlpool', '-blake2s256']


openssl_path = ['/usr/bin/openssl']

crctk_path = ['/usr/bin/crctk']

skip_crc32 = False

output_file = 'data.txt'

data = []

##################################################
#           Error Checking Functions               
##################################################

def check_errors():
    # Performs checks to ensure we have everything we need
    # Executes: check_platform(), check_openssl(), check_files()

    global file_list

    check_platform()
    check_openssl()
    check_crctk()

    if (check_files(file_list) == False):
        print("[!] File path issues found, please fix & try again")
        sys.exit(1)
    
def check_platform():
    # Checks whether we're on Linux

    if (sys.platform == 'linux' or sys.platform == 'linux2'):
        pass
    else:
        print("[!] Only Linux platform is supported")
        sys.exit(1) 


def check_openssl():
    # Checks if openssl is available

    global openssl_path

    if (check_files(openssl_path) == False):
        print("[!] Openssl not found")
        sys.exit(1)

def check_crctk():
    # Checks if crctk is installed

    global crctk_path, skip_crc32

    if (check_files(crctk_path) == False):
        print("[!] crctk not found")
        val = input("[?] Do you want to continue? y/N").strip().lower()

        if (val == 'y' or val == 'yes'):
            skip_crc32 = True
            print("[*] Skipping crctk hash checks")
        else:
            sys.exit(1)

def check_files(files=[]):
    # Iterates over file_list, to verify they exist
    # Returns: Boolean indicating whether all paths are valid files

    if (files != []):
        for f in files:
            if (os.path.isfile(f)):
                pass
            else:
                #print("File %s doesn't exist." % f)
                return False 
        return True


##################################################
#               Core Functions           
##################################################

def print_intro():
    print("*"*50)
    print("HashBenchmark.py")
    print("*"*50)
    print()
          
def run_cmd(cmd=[]):
    # Executes bash commands on local Linux system

    if (cmd != []):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
               stderr=subprocess.PIPE)

        stdout,stderr = process.communicate()

        stdout = stdout.decode('ascii').strip()
        stderr = stderr.decode('ascii').strip()

        return stdout,stderr

def check_hashes():
    # Executes openssl hashing function on all files
    # md5, sha1, sha224, sha3-256, sha-256, 
    # ripemd, whirlpool, blake2s256
    
    global file_list, openssl_hash_types, skip_crc32, data
    
    for i in openssl_hash_types:
        print("Hash type: %s" % (i.upper().replace("-", "")))
        _hash = i.upper().replace('-',"")
        _total_time = 0.0

        for f in file_list:
            start_time = time.time()
            stdout,stderr = run_cmd(['openssl', 'dgst', i, f])
            end_time = time.time()
            total_time = end_time - start_time
            print(stdout)
            print("File: %s" %f)
            print("Time taken: %.2f s\n" % total_time)

            _total_time += total_time

        time_per_GB = (_total_time/12.0)
            
        print("Time / GB: %.2f s\n" % time_per_GB)
        print("#"*50)
        
    # Checking for crc32 hash
    if (skip_crc32 != True):
        print("Hash type: CRC-32")

        _total_time = 0.0

        for f in file_list:
            start_time = time.time()
            stdout,stderr = run_cmd(['crctk', '-c', f])
            end_time = time.time()
            total_time = end_time - start_time
            _total_time += total_time
            print(stdout)
            print("File: %s" % f)
            print("Time taken: %.2f s\n" % total_time)

        time_per_GB = (_total_time/12.0)
                
        print("Time / GB: %.2f s\n" % time_per_GB)
    
    print("#"*50)


if __name__ == '__main__':
    print_intro()

    try:
        check_errors()
        check_hashes()
    except(KeyboardInterrupt):
        sys.exit(1)



