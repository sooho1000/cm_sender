#!/usr/bin/env python

''' 
python-tail example.
Does a tail follow against /var/log/syslog with a time interval of 5 seconds.
Prints recieved new lines to standard out '''

import ftp
import log
import tail
from datetime import datetime

f = ftp.FTP()

def send_cm(fpath, fname):
    f.send_file(fpath, fname)
    
def find_string(txt):
    search = "Success to store stream"
    if search in txt:
        po = txt.find("FilePathName:")
        path = txt[po+14:-2]
        paths = path.split('\\')
        if paths[1] == "CM":
            file_name = paths[-1]
            del paths[-1:]
            file_path = "\\".join(paths)
            logger.info("[find_string] - " +  file_path + "\\" + file_name)
            send_cm(file_path, file_name)

if __name__ == "__main__":
    logger = log.get_logger()

    t = tail.Tail('')
    t.register_callback(find_string)
    while True:
        log_file_path = r"C:\KONAN\TransferManager_FTP\log"
        log_file_name = "KFTPServer_" + datetime.today().strftime("%Y%m%d") + ".txt"

        t.set_tailed_file(log_file_path + "\\" + log_file_name)
        t.set_today()
        t.reset_curr_position()
        t.follow(s=5)
