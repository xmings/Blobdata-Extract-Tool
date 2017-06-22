#-*- coding:utf-8 -*-
import os, sys, time
import datetime, re, cx_Oracle
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
            print(u"参数文件配置有误!!!")
                    
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


class ToolBox(object):
    def __init__(self):
        pass
    
    @staticmethod
    def recordNumber(file, num):
        with open(file, 'a') as f:
            text = str(num) + ' rows exported at ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) + '\n'
            f.write(text)
    
    @staticmethod        
    def formartImageName(strs):
        strs = str(strs)
        while strs.find('*')>0 and not strs.endswith('*'):
            strs = strs.replace('*','×')
    
        strs = strs.replace('*','').replace('@','').replace('<','').replace('>','')\
            .replace('/','').replace('?','').replace('|','').replace('"','')\
               .replace('\r','').replace('\t','').replace('\n','').replace(' ','')
    
        return strs if strs else ''
    
    @staticmethod
    def getFileCount(filePath, logFileName):
        lineCount = 0
        for f in os.listdir(filePath):
            if logFileName.split('N')[0] in f:
                logFile = os.path.join(filePath, f) 
                winCmd = "type " + logFile + "|find /c /v \"\""
                lineCount += int(os.popen(winCmd).readline().replace('\n',''))
        return lineCount
    
    @staticmethod
    def createDir(filePath, dirCount):
        subDirCount = 0
        for i in range(dirCount):
            subDir = os.path.join(filePath, str(i+1))
            if os.path.exists(subDir) and os.path.isdir(subDir):
                continue
            os.mkdir(subDir)
            
    @staticmethod
    def genImageName(infoList, infoIndexList, imageNameSpliter):
        imageName = ''
        ind = 0
        for i in infoIndexList:
            if i == -1:
                continue
            index = infoIndexList.index(ind)
            imageName += infoList[index] + imageNameSpliter
            ind += 1
        return imageName.rstrip(imageNameSpliter)
    
    @staticmethod
    def genColumnValueStr(infoList, infoIndexList):
        columnValueStr = ""
        ind = 0
        for i in infoIndexList:
            if i == -1:
                continue
            index = infoIndexList.index(ind)
            if isinstance(infoList[index], cx_Oracle.LOB):
                columnValueStr += ":blobData" + ","
            elif isinstance(infoList[index], str):
                columnValueStr += "'" + infoList[index] + "',"
            elif isinstance(infoList[index], [int,long,float,complex]):
                columnValueStr += str(infoList[index]) + ","
            else:
                print(infoList[index], type(infoList[index]))
            
            ind += 1
        return columnValueStr.rstrip(',')        
        
            
    
        
        

if __name__ == '__main__':
    paraprase = ParaPrase.get()
    