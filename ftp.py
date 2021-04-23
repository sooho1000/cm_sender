import datetime
import ftplib
import log
import os

class FTP(object):
    def __init__(self):
        self.id = "ftpuser"
        self.passwd = "1234qwer"
        # self.ip = "10.9.110.43"
        self.ip = "10.40.10.97"
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.ip, 21)
        self.ftp.login(self.id, self.passwd)
        self.ftp.encoding = "utf-8"
        self.logger = log.get_logger()

    def exist(self, fname):
        if fname in self.ftp.nlst():
            return True
        return False

    def chdir(self, fpath):
        for path in fpath.split('/'):
            if self.exist(path):
                self.ftp.cwd(path)
            else:
                self.ftp.mkd(path)
                self.ftp.cwd(path)

    def send_file(self, source_path, filename):
        filepath = "CM_EMR"
        now = datetime.datetime.now() # 2018-07-28 12:11:32.669083
        nowDate = now.strftime('%Y-%m-%d') # 2018-07-28
        self.chdir(filepath + "/" + nowDate)

        os.chdir(source_path)
        myfile = open(filename,'rb')
        self.logger.info("[SEND FILE Start] filename : " + filename)
        self.ftp.storbinary('STOR ' +filename, myfile)
        self.logger.info("[SEND FILE end]")
        myfile.close()
        self.ftp.close