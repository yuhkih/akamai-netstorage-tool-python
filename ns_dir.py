# ----------------------------------------
# Name: ns_dir.py
# Perupose: dir only root (/CPCODE ) directory
# 2019/01/08 yuhki initial release
# ----------------------------------------

import optparse, sys, json, os
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from akamai.netstorage import Netstorage

class NetstorageParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

# Degug flag
DEBUG = 0 # (1:DEBUG, 0:Non DEBUG)


# epoch to date
def epoch_to_datetime(epoch):
    return datetime(*time.localtime(epoch)[:6])


def debug_result(response, action):
    print("[DEBUG] ----- Request Header -----")
    print(response.request.headers)
    print("[DEBUG] ----- Response Code -----")
    print(response.status_code)
    print("[DEBUG] ----- Response Header -----")
    print(response.headers)
    if action != 'download':
        print("[DEBUG] ----- Response Content -----")
        print(response.text)


# ---------------------------------------------
# Read NetStorage Credential File
# ---------------------------------------------

# Check if a ns_credential file exists
credential_file = "./ns_credential.txt"
if os.path.exists(credential_file):
    file = open('ns_credential.txt','r')
    lines = file.readlines()
    file.close
else:
    print("[ERROR]Please put credential file for NetStorage and name it ns_credential.txt and place it in the same directory")
    exit()

file = open('ns_credential.txt','r')
lines = file.readlines()
file.close

# Read the ns_credential.txt
for line in lines:
    if line.find("hostname") >=0:
        hostname = line[:-1].split(" ")[2]
        # shostname = 'shostname=' + hostname
        # print(shostname)
    if line.find("username") >=0:
        username = line[:-1].split(" ")[2]
        # susername = 'username=' + username
        # print(susername)
    if line.find("key") >=0:
        key = line[:-1].split(" ")[2]
        # skey = "key=" + key
        # print(skey)
    if line.find("cpcode") >=0:
       cpcode = line[:-1].split(" ")[2]
       # scpcode = "cpcode=" + cpcode
       # print (scpcode)


args = sys.argv
subdirectory = ""
if len(args) > 1:
    subdirectory = args[1]

if __name__ == '__main__':

    ns = Netstorage(hostname, username, key)
    res = None

    # ---------------------------------------------
    # dir
    # ---------------------------------------------
    directory = "/"

    if len(subdirectory) != 0:
        directory = directory + subdirectory

    print("[LOG] dir directory", directory)
    action = "dir"    

    directory = "/" + cpcode + directory
    print("[LOG] true directory", directory)

    ok, res = ns.dir(directory)

    # Analyze return information
    if ok == True :
        print("[LOG] dir succeeded")
        print("[LOG] ------------------------------")        
    else:
        print("[LOG] dir failed:", res.text)
        exit()

    if DEBUG == 1:
        debug_result(res,action)    

    # Parse XML object
    root = ET.fromstring(res.text)
    # Child 
    for child in root:
        # print(child.tag, child.attrib)
        filename = child.attrib['name']
        print(filename, epoch_to_datetime(int(child.attrib['mtime']))) # Time