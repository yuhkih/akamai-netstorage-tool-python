# Akamai NetStorage API tools

# Prepartion
1. prepare "ns_credential.txt" and put it in the same directory with the scipts.  
   See ns_credential.txt.sample for the format.  
2. Execute script  
  
# How to use  
 
### Dir specfied directory
*ns_dir.py* - return files and directories under <CPCODE>/
*ns_dir.py <dirname>* - retunrn files and directory under <CPCODE>/<dirname>  
examples:  
ns_dir.py test - return files and directory under <CPCODE>/test  
ns_dir.py dir/test - return files and directory under <CPCODE>/dir/test  

### Download all the file <CPCODE>/ directory 
*ns_download.py*  
example:  
python ns_download.py  
   
### Download all the file <CPCODE>/ directory then move the downloaded files to <CPCODE>/downloaded directory  
*ns_download_move.py*  
example:  
python ns_download_move.py  
   
### Download all the file <CPCODE>/ directory then delete the downloaded files
*ns_download_delete.py*  
example:  
python ns_download_move.py  - interactive mode
python ns_download_move.py y - non interactive mode   
   
### Delete specified file  
*ns_delete.py  <filename>*  
example:  
python ns_delete.py mylogfile.log
   
  
# confirmed in the following environment  
Python 2.7.14 (windows)  
Python 3.6.3 (windows)
NetStorage 4 (NS4). (Not sure this works with NS3)  
