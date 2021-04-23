import datetime
import ftplib
import json
import log
import os

class FTP(object):
    def __init__(self):
        self.logger = log.get_logger()
        with open("config.json", 'r') as c:
            config = json.load(c)
        self.servers = config['SERVER_LIST']
        self.id = config['ID']
        self.passwd = config['PASSWD']
        self.ftp = ftplib.FTP()

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

    def send_done_file(self, filename):
        done_file = open(filename + ".done", 'w')
        done_file.close()
        done_file = open(filename + ".done",'rb')
        self.logger.info("[Send Done file start] " + filename)
        self.ftp.storbinary('STOR ' +filename + ".done", done_file)
        self.logger.info("[Send Done file end]")
        done_file.close()
        os.remove(filename + ".done")

    def send_file(self, source_path, filename):
        os.chdir(source_path)
        self.logger.debug(os.getcwd())
        myfile = open(filename,'rb')
        for server in self.servers:
            self.logger.info("To : " + server)
            self.ftp.connect(server, 21)
            self.ftp.login(self.id, self.passwd)
            self.ftp.encoding = "utf-8"
            filepath = "CM_EMR"
            now = datetime.datetime.now() # 2018-07-28 12:11:32.669083
            nowDate = now.strftime('%Y-%m-%d') # 2018-07-28
            self.chdir(filepath + "/" + nowDate)
            self.logger.info("[SEND FILE Start] filename : " + filename)
            self.ftp.storbinary('STOR ' +filename, myfile)
            self.logger.info("[SEND FILE end]")
            myfile.close()
            self.send_done_file(filename)
            self.ftp.close()