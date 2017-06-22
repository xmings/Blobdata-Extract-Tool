#-*- coding:utf-8 -*-
import cx_Oracle
import os, sys, time
import datetime, re
from DBConn import DBConnection
from Util import ToolBox
from multiprocessing import Process, Pool, Queue

class DBWriter(object):
	def __init__(self, dbConnStr, commitCount = 1000):
		self.db = DBConnection(dbConnStr)
		self.cursor = self.db.openConnection()
		self.count = 0
		self.cursor.setinputsizes(blobData=cx_Oracle.BLOB)
		self.commitCount = commitCount

	def run(self, insertSQLStr, blob):
		self.count += 1
		self.cursor.execute(insertSQLStr, {'blobData':blob})
		if self.count % self.commitCount == 0:
			self.db.connection.commit()

	def close(self):
		self.db.connection.commit()
		self.cursor.close()
		self.db.connection.close()
		

if __name__ == '__main__':
	sqlStr = "insert /*+append*/ into test_target(XM,SFZHM,PIC) values ('bbb','7890123',:blobData )"
	db = DBWriter('system/oracle@orcl')
	
	with DBConnection('system/oracle@orcl') as testdb:
		cursor = testdb.openConnection()
		cursor.execute('select zp from TEST_image')
		res = cursor.fetchone()
		db.run(sqlStr, res[0].read())
	db.close()
	
		
		

	









