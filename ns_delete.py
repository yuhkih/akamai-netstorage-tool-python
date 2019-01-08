# ----------------------------------------
# Name: ns_delete.py
# Perupose: delte specified file
# 2019/01/08 yuhki initial release
# ----------------------------------------
import optparse, sys, json, os
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from netstorage import Netstorage

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

args = sys.argv
delete_file = args[1]

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


if __name__ == '__main__':

    # User setting
  #  hostname = "yhanada-ns4-1-nsu.akamaihd.net"
  #  username = "yhanada1"
  #  key = "VOOhNCvmwBvwfvj843yuyWnosgnCjmnGlTYAAjP3hng1q"
  #  cpcode = "673558"

    ns = Netstorage(hostname, username, key)
    res = None

    # ---------------------------------------------
    # Execute Delete
    # ---------------------------------------------
    delete_file = "/" + cpcode + "/" + delete_file
    print("[LOG] delete file:[",delete_file, "] will be deleted")
    action = "delete" 
    
    # Execute delete
    ok, res = ns.delete(delete_file)

    # Analyze return information
    if ok == True :
        print("[LOG] File sucessfully deleted")
    else:
        print("[LOG] File deletion failed:", res.text)

    if DEBUG == 1:
        debug_result(res,action)    
