import os, sys, time
import datetime, re
from configparser import ConfigParser, Error, RawConfigParser

_CONFIG_FILE = 'config.ini'

PRO_DIR = os.path.abspath('.')

class ParaPrase(object):
    paraprase = ''
    def __init__(self):
        pass
    @classmethod
    def get(cls):
        if cls.paraprase:
            return cls.paraprase
        try:
            config = ConfigParser(delimiters=('='), comment_prefixes=('#'), inline_comment_prefixes=('#'))
            config.read(_CONFIG_FILE, encoding='utf-8')
            cls.paraprase = config
            return cls.paraprase
        except Error:
            print("参数文件配置有误!!!")
                    
    @staticmethod    
    def get_spliter(t):
        spliterpara = ParaPrase.get()
        default = {'rowspliter': ';;;', 'colspliter': '*-*',}
        return spliterpara['DATA'][t] if spliterpara['DATA'].get(t) else default[t]
    
    @staticmethod
    def get_other(section, key):
        spliterpara = ParaPrase.get()
        try:
            return spliterpara[section].get(key)
        except:
            #sample_config = """
                        #[DATABASE]
                        #dbconn =
                        #nls_lang =
            
                        #[TABLE]
                        #importtable=
                        #exportsqlstr=
            
                        #[DATA]
                        #rowspliter=
                        #colspliter=
            
                        #[PICTURE]
                        #piccolumn=
                        #picnamecolumn=
                        #picnamespliter=
                        #picpath=
            
                        #[FILE]
                        #datafile=
                        #logfile=
                        #controlfile="""            
            #config = ConfigParser.RawConfigParser(allow_no_value=True)
            #config.readfp(io.BytesIO(sample_config))            
            return ""
    @staticmethod
    def set(section, key, value):
        conf = ParaPrase.get()
        conf.set(section, key, value)
        conf.write(open(_CONFIG_FILE, 'w'))    
        

class WriteFile(object):
    def __init__(self, iopath):
        self.iopath = iopath
    
    def writepic(self, filename, data, t='txt'):
        writemode = 'w' if t == 'txt' else 'wb'
        filepath = os.path.join(self.iopath, filename)
        with open(filepath, writemode) as file:
            file.write(data)
            
          

class ReadFile(object):
    def __init__(self, iopath):
        self.iopath = iopath
        # 文件记数器
        self.fid = 0        

    def scanpics(self, spliter=None):
        for picname in os.listdir(self.iopath):
            print(picname)
            prepicname = os.path.splitext(picname)[0]
            picpath = os.path.join(self.picpath, picname)
            self.data = ''
            with open(picpath, 'rb') as pic:
                self.data = pic.read()
            self.fid += 1
                
            yield [self.fid, prepicname, self.data]
            

class WriteLog(object):
    pass



class ToolBox(object):
    def __init__(self):
        pass
    @staticmethod
    def get_sqluldr(parent):
        files = [ 'sqluldr2.lib','sqluldr2.dll','sqluldr2.exe' ]  #必备文件
        
        for filename in files:
            if not os.path.exists(os.path.join(PRO_DIR, filename)):
                parent.displaylog("sqluldr模块不完整")
                raise Exception("sqluldr模块不完整")
        return os.path.join(PRO_DIR, 'sqluldr2.exe')
    
    @staticmethod
    def recordnumber(file, num):
        with open(file, 'a') as f:
            text = str(num) + ' rows exported at ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) + '\n'
            f.write(text)        
        

class DBIOException(Exception):
    def __init__(self, args):
        self.args = args
        

if __name__ == '__main__':
    paraprase = ParaPrase.get()
    