#-*- coding:utf-8 -*-
import cx_Oracle
import os, sys, time
import datetime, re
from DBConn import DBConnection
from Util import ToolBox
from multiprocessing import Process, Pool, Queue

class DBWriter(object):
	def __new__(cls, *args, **kw):  
		if not hasattr(cls, '_instance'):  
			cls._instance = object.__new__(cls, *args, **kw)  
		return cls._instance  	
	
	def __init__(self, dbConnStr):
		self.db = DBConnection(dbConnStr)
		self.cursor = self.db.openConnection()
		self.count = 0
		self.commitCount = 1000
	
	def run(self, insertSQLStr, blob):
		self.count += 1
		self.cursor.setinputsizes(blobData=cx_Oracle.BLOB)
		self.cursor.execute(insertSQLStr, {'blobData':blob})
		if self.count % self.commitCount == 0:
			self.db.connection.commit()
			
	def close(self):
		self.db.connection.commit()
		self.cursor.close()
		self.db.connection.close()
	

class Blob2DB(object):
	def __init__(self, sourceDBConnStr, targetDBConnStr,
	             blobIdSQLStr, blobSQLStr, blobInsertSQLStr,
	             columnPositionList, processes = 6, mode = 0):
		# mode=0不需要和已抽取的图片ID比对; 
		# mode=1当程序中断后，需要关联已抽取的图片ID来抽取剩余图片
		self.sourceDBConnStr = sourceDBConnStr
		self.targetDBConnStr = targetDBConnStr
		self.blobIdCount = 0
		self.blobIdSQLStr = blobIdSQLStr
		self.blobSQLStr = blobSQLStr
		self.blobInsertSQLStr = blobInsertSQLStr
		self.columnPositionList = columnPositionList
		self.processes = processes
		self.mode = mode
		
		self.init()

	def init(self):
		if self.blobIdCount == 0:
			self.getBlobIdCount()

	def getBlobIdCount(self):
		sqlStr = "select count(1) from " + re.split('from', self.blobIdSQLStr, flags= re.I)[1]
		with DBConnection(self.sourceDBConnStr) as dbConnection:
			cursor = dbConnection.openConnection()
			cursor.execute(sqlStr)
			self.blobIdCount = cursor.fetchone()[0]
		return self.blobIdCount

	def setBlobIdCount(self, count):
		self.blobIdCount = count


	def master(self, imgQueue):
		"""获取所有图片记录的ROWID及图片名称，放入队列"""
		
		with DBConnection(self.sourceDBConnStr) as dbConnection:
			cursor = dbConnection.openConnection()
			cursor.execute(self.blobIdSQLStr)
			for res in cursor:
				imgQueue.put(res)
			imgQueue.put(["gameover",0])


	def slave(self, imgQueue):
		"""从队列中取出ROWID，再到图片表获取图片数据并再OS上生成图片文件"""
		self.targetDB = DBWriter(self.targetDBConnStr)
		print(self.targetDB)
		with DBConnection(self.sourceDBConnStr) as dbConnection:
			cursor = dbConnection.openConnection()
			while True:
				imageIdInfo = imgQueue.get()
				imageId = imageIdInfo[0]
				if imageId == "gameover":
					imgQueue.put(["gameover",0])
					break
				sqlStr = self.blobSQLStr % (str(imageId))
				cursor.execute(sqlStr)
				res = cursor.fetchone()
				if res and res[0]:
					blobNameColumnList = imageIdInfo + res[:]
					columnValueStr = ToolBox.genColumnValueStr(blobNameColumnList, self.columnPositionList)
					blobInsertSQLStr = self.blobInsertSQLStr + ' ( ' + columnValueStr + ' )'
					self.targetDB.run(blobInsertSQLStr, res[0].read())
		self.targetDB.close()
		
	def dbWriter(self, dbwQueue):
		pass
		
					
		
				

	



if __name__ == "__main__":        
	print("goo.....")
	# 开启一个全局的对列，用于下面存放图片ROWID
	imgQueue = Queue()
	expRecQueue = Queue()
	blob2db = Blob2DB('scott/tiger@orcl')
	allProcesses = []

	master = Process(target=blob2db.master,args=(imgQueue,))
	master.start()
	allProcesses.append(master)
	record = Process(target=blob2db.recordBlobId,args=(expRecQueue,))
	record.start()
	allProcesses.append(record)



	for i in range(6):
		slave = Process(target=blob2os.slave,args=(imgQueue, expRecQueue,))
		slave.start()
		allProcesses.append(slave)


	for slave in allProcesses:
		slave.join()

	gc.collect()










