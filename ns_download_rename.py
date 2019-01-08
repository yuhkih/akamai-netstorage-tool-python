# ----------------------------------------
# Name: ns_download_move.py
# Perupose: Download log file then move to other directory
# 2019/01/08 yuhki initial release
# ----------------------------------------
import optparse, sys, json,os
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from akamai.netstorage import Netstorage

class NetstorageParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog


# Degug flag
DEBUG = 0 # (1:DEBUG, 0:Non DEBUG)
movedir = "downloaded" # move target directory

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

if __name__ == '__main__':

    ns = Netstorage(hostname, username, key)
    res = None

    # ---------------------------------------------
    # Get List
    # ---------------------------------------------
    print("[LOG] getting list")
    action = "dir"
    
    cpcode = "/" + cpcode
    ok, res = ns.dir(cpcode)
    print(res.text)

    # Check result
    if ok == True :
        print("[LOG] dir succeeded")
        print("[LOG] ------------------------------")                       

        # Parse XML object
        root = ET.fromstring(res.text)
        # Child 
        for child in root:
            filename = child.attrib['name']
            print(filename, epoch_to_datetime(int(child.attrib['mtime']))) # Time

        # ---------------------------------------------
        # Download file
        # ---------------------------------------------
        for child in root:
            filename = child.attrib['name']
            action = "download"
            pathfilename = cpcode + "/" + filename

            # Download file
            ok, res = ns.download(pathfilename)

            if ok == True :
                print("[LOG] Downlaod succeeded",pathfilename)

                # ---------------------------------------------
                # Move file (correctly specaking, rename file)
                # If there isn't target directory, the directory will be created.
                # ---------------------------------------------
                action = "rename"
                newfilename = "/673558/" + movedir + "/" + filename
                ok, res = ns.rename(pathfilename, newfilename)
            
                if ok == True :
                    print("[LOG] Move succeeded",newfilename)
                else:
                    print("[LOG] Move Failed. Abort",newfilename)
                    exit()
        
        else:
             print("[LOG] Downlaod Failed",pathfilename)
             exit()

    else:
        print("[LOG] dir failed:", res.text)
        exit()

  
 