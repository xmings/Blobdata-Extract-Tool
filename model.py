#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<wangms>
  Purpose:  --make the sqluldr2 better use than before
  Created: 2016-4-2
"""

import os, sys, Tkinter
import threading
from time import ctime,sleep


curr_dir =  os.path.abspath('.')
sqluldr2 = [ 'sqluldr2.lib','sqluldr2.dll','sqluldr2.exe' ]  #必备文件

for filename in sqluldr2:
    if not os.path.exists(os.path.join(curr_dir, filename)):
        print u"sqluldr2工具不存在"
    else:
        pass
    
    
class MutiThreadReadLog(object):
    def __init__(self, parent, filename, **kwargs):
        self.parent = parent
        self.filename = filename
        self.kwargs = kwargs
        self.threads = []
        
    def readLog(self):
        while True:
            sleep(2)
            self.alivethread = 0
            for i in range(len(self.threads)):
                if self.threads[i].is_alive():
                    self.alivethread = self.alivethread + 1
                    
            self.readfile = open(self.filename, 'r')
            self.readcontent = self.readfile.read()
            self.readfile.close()            
            self.parent.logtext.delete('0.0', Tkinter.END)
            self.parent.logtext.insert('0.0', self.readcontent)
            
            if self.alivethread == 1:   #剩下的这个进程为读日志线程
                print u"所有抽取或加载已结束，日志读取也即将结束"
                break                

            

    def run(self):
        for k in self.kwargs:
            if k.startswith('thread'):   
                t1 = threading.Thread(target=self.kwargs[k])
                self.threads.append(t1)
  
        for t in self.threads:
                t.setDaemon(True)
                t.start()         

class ExtractData(MutiThreadReadLog):
    def __init__(self, parent, user, query, field, datafile, logfile, ctlfile, imptable, impmethod, islob):
        self.parent = parent
        self.user = u' user=' + user
        self.query = u' query="' + query + '"'
        self.field = u' field=' + field
        self.datafile = u' file=' + datafile
        self.logfile = u' log=' + logfile
        self.ctlfile = u' control=' + ctlfile if ctlfile else ''
        self.imptable = u' table=' + imptable if imptable else ''
        self.mode = u' mode=' + impmethod if impmethod else ''
        self.lob = u' LOB=' + 'FILE' if islob else ''
        self.degree = u' degree=8'
        
        print logfile
        super(ExtractData, self).__init__(self.parent, logfile, thread1=self.extractData, thread2=self.readLog)
        
        #self.run()
        

    def extractData(self):
          
        self.option = self.user \
            + self.query \
            + self.field \
            + self.datafile \
            + self.logfile \
            + self.imptable \
            + self.ctlfile \
            + self.mode \
            + self.lob \
            + self.degree
        
        self.option = self.option.replace('\n', '')
        self.option.replace('\n', '')
        print self.option
        try:
            os.system(os.path.join(curr_dir, 'sqluldr2.exe') +' '+self.option)
        except:
            print u"抽数异常，请查看日志！！！"
            
            
   
        
class LoadData(MutiThreadReadLog):
    def __init__(self, parent, userid, controlfile, **args):
        self.parent = parent
        self.userid = u' userid=' + userid
        self.controlfile = u' control=' + controlfile
        self.logfile = u' log=' + os.path.join(os.path.dirname(controlfile), 'implogfile.log')
        
        super(LoadData, self).__init__(self.parent, self.logfile, thread1=self.extractData, thread2=self.readLog)
    def loaddata(self):
        self.option = self.userid \
            + self.controlfile \
            + ' direct=TRUE'

        self.option = self.option.replace('\n', '')
        self.option.replace('\n', '')
        print self.option
        try:
            os.system('sqlldr' +' '+self.option)
        except:
            print u"加载异常，请查看日志！！！"        
            


