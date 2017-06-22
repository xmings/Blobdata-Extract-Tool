#-*- coding:utf-8 -*-
import cx_Oracle
import os, sys, time
import datetime, re
from DBConn import DBConnection
from Util import ToolBox
from multiprocessing import Process, Pool, Queue

class Blob2OS(object):
    def __init__(self, sourceDBConnStr, blobIdSQLStr, \
                 blobSQLStr, filePath, blobNameColumnIndexList, \
                 blobNameSpliter = '_', processes = 6, subDirCount= 0 , mode = 0):
        # mode=0不需要和已抽取的图片ID比对; 
        # mode=1当程序中断后，需要关联已抽取的图片ID来抽取剩余图片
        self.sourceDBConnStr = sourceDBConnStr
        self.blobIdCount = 0
        self.blobIdSQLStr = blobIdSQLStr
        self.blobSQLStr = blobSQLStr
        self.filePath = filePath if filePath else os.path.abspath('.')
        self.blobNameColumnIndexList = blobNameColumnIndexList
        self.blobNameSpliter = blobNameSpliter
        self.subDirCount = subDirCount
        self.processes = processes
        self.mode = mode
        self.logFileName = 'exp_record_N.log'
        self.init()
        
    def init(self):
        if self.subDirCount == 0:
            if self.blobIdCount == 0:
                self.getBlobIdCount()
            self.getSubDirCount()
            
        ToolBox.createDir(self.filePath, self.subDirCount)
        
    def getBlobIdCount(self):
        sqlStr = "select count(1) from " + re.split('from', self.blobIdSQLStr, flags= re.I)[1]
        with DBConnection(self.sourceDBConnStr) as dbConnection:
            cursor = dbConnection.openConnection()
            cursor.execute(sqlStr)
            self.blobIdCount = cursor.fetchone()[0]
        return self.blobIdCount
            
    def setBlobIdCount(self, count):
        self.blobIdCount = count
        
    def getSubDirCount(self, perCount = 100000):
        self.subDirCount = self.blobIdCount / perCount + 1 \
            if self.blobIdCount % perCount > 0 else self.blobIdCount % perCount
        
    def master(self, imgQueue):
        """获取所有图片记录的ROWID及图片名称，放入队列"""
        with DBConnection(self.sourceDBConnStr) as dbConnection:
            cursor = dbConnection.openConnection()
            cursor.execute(self.blobIdSQLStr)
            fileNo = ToolBox.getFileCount(self.filePath, self.logFileName)
            for res in cursor:
                fileNo += 1
                data = res + (fileNo, )
                imgQueue.put(data)
            imgQueue.put(["gameover",0])


    def slave(self, imgQueue, recQueue):
        """从队列中取出ROWID，再到图片表获取图片数据并再OS上生成图片文件"""
        with DBConnection(self.sourceDBConnStr) as dbConnection:
            cursor = dbConnection.openConnection()
            
            while True:
                imageIdInfo = imgQueue.get()
                imageId = imageIdInfo[0]
                fileNo = imageIdInfo[-1]
                if imageId == "gameover":
                    imgQueue.put(["gameover",0])
                    recQueue.put("gameover")
                    break
                sqlStr = self.blobSQLStr % (str(imageId))
                cursor.execute(sqlStr)
                res = cursor.fetchone()
                if res and res[0]:
                    blobNameColumnList = imageIdInfo[:-1] + res[:]
                    print(imageIdInfo)
                    imageName = ToolBox.genImageName(blobNameColumnList,
                                                     self.blobNameColumnIndexList,
                                                     self.blobNameSpliter)
                        
                    fileName = os.path.join(self.filePath,
                                            str(fileNo % self.subDirCount + 1) ,
                                            imageName + self.blobNameSpliter + str(fileNo) + '.jpg')                    
                
                    try:
                        with open(fileName,'wb') as f:
                            f.write(res[0].read())
                    except Exception as e:
                        print(e.args)
                        with open(ToolBox.formartImageName(fileName), 'wb') as f:
                            f.write(res[0].read())
                        print("imageId: "+ str(imageId) + " has settled")
    
                recQueue.put(imageId)

    def recordBlobId(self, recQueue):
        overCount = 0
        queueIsLive = True
        recordNo = 0
        logFileNo = 0
        logFile = self.filePath
    
        while queueIsLive:
            while os.path.exists(logFile):
                logFileNo += 1;
                logFile = os.path.join(self.filePath, self.logFileName.replace('N',str(logFileNo)))
    
            print(logFile)
    
            with open(logFile, 'w+') as f:
                while True:
                    imageId = recQueue.get()
                    if str(imageId) == "gameover":
                        overCount +=1
                        if overCount >= self.processes:
                            queueIsLive = False
                            break
                    f.write(str(imageId)+'\n')
                    recordNo += 1;
    
                    if recordNo % 5000000 == 0:
                        print('export 5000000')
                        break




if __name__ == "__main__":        
    print("goo.....")
    # 开启一个全局的对列，用于下面存放图片ROWID
    imgQueue = Queue()
    expRecQueue = Queue()
    blob2os = Blob2OS('scott/tiger@orcl')
    allProcesses = []

    master = Process(target=blob2os.master,args=(imgQueue,))
    master.start()
    allProcesses.append(master)
    record = Process(target=blob2os.recordBlobId,args=(expRecQueue,))
    record.start()
    allProcesses.append(record)



    for i in range(6):
        slave = Process(target=blob2os.slave,args=(imgQueue, expRecQueue,))
        slave.start()
        allProcesses.append(slave)


    for slave in allProcesses:
        slave.join()

    gc.collect()










