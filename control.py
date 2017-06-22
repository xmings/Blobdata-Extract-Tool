# -*- coding: utf-8 -*-
import re, cx_Oracle
from DBConn import DBConnection
from Util import ToolBox
from Blob2OS import Blob2OS
from Blob2DB import Blob2DB, DBWriter
from multiprocessing import Process, Pool, Queue, cpu_count

class Control(object):
	def __init__(self):
		self.sourceDBConnStr = ''
		self.targetDBConnStr = ''
		self.blobIdSQL = ''
		self.blobSQL = ''
		self.targetTable = ''
	
	def getDBConnStatus(self, dbConnStr, t = 'sourceDB'):
		result = ''
		with DBConnection(dbConnStr) as db:
			result = db.openConnection()
		
		if  t == 'sourceDB':
			self.sourceDBConnStr = dbConnStr
		else:
			self.targetDBConnStr = dbConnStr
			
		return result
	
	def getSourceTableColumnName(self, blobIdSQL, blobSQL):
		self.columnNameList = []
		if blobIdSQL:
			p1 = re.split('from', blobIdSQL, flags = re.I)[0]
			p1 = re.sub('select', '', p1, count = 1, flags = re.I).strip(' ').split(',')
			for p2 in p1:
				p3 = re.split(' |as', p2, flags = re.I)
				if not p3:
					continue
				p3 = 'SQL1.' + p3[-1]
				self.columnNameList.append(p3)
			self.blobIdSQL = blobIdSQL
			
		if blobSQL:
			p1 = re.split('from', blobSQL, flags = re.I)[0]
			p1 = re.sub('select', '', p1, count = 1, flags = re.I).strip(' ').split(',')
			for p2 in p1:
				p3 = re.split(' |as', p2, flags = re.I)
				if not p3:
					continue			
				p3 = 'SQL2.' + p3[-1]
				self.columnNameList.append(p3)
			self.blobSQL = blobSQL	
		
		return self.columnNameList
			
	
	def getTargetTableColumn(self, tableName):
		self.targetTable = tableName
		tableColumn = []
		with DBConnection(self.targetDBConnStr) as db:
			cursor = db.openConnection()
			if cursor:
				cursor.execute("select * from " + tableName)
				tableColumn = [i[0] + ' ' + str(i[1]).replace("type 'cx_Oracle.", "")\
				               .replace("'", "") for i in cursor.description]
		return tableColumn
		
	
	def genFetchBlobSQL(self, blobIdColumn, blobColumn, blobNameColumnList, blobNameSpliter):
		tableName = []
		blobIdColumn
		tableName.append(self.getTableNameAndColumnName(blobIdColumn)[0])
		for i in blobNameColumnList:
			table = self.getTableNameAndColumnName(blobIdColumn)[0]
			if tableName.count(table) == 0:
				tableName.append(table)
		
		if len(tableName) == 1:
			blobIdSQLStr = "Select base." + self.getTableNameAndColumnName(blobIdColumn)[1] + " , " \
					    + ",".join([" base." + self.getTableNameAndColumnName(i)[1] for i in blobNameColumnList]) \
			            + " From " + tableName[0] + " base"
			blobSQLStr = "Select blob." + self.getTableNameAndColumnName(blobColumn)[1] + " from " + tableName[0]	+ " blob where "		
		elif len(tableName) >= 2:
			blobTableName,blobColumn = self.getTableNameAndColumnName(blobColumn)
			
		else:
			pass
		
		
		
		if len(tableName) == 1:
			pass
		else:
			blobTable = blobColumn.split('.')[0]
			blobColumn = blobColumn.split('.')[1]
			baseTable = tableName.pop(blobTable)[0]
			
		return blobIdSQLStr, blobSQLStr
	
	def getTableNameAndColumnName(self, tableColumn):
		owner, table, column = tableColumn.split('.') \
		    if tableColumn.count('.') == 2 else ['', ] + tableColumn.split('.')
		tableName = owner + '.' + table if owner else table
		
		return tableName, column
	
	
	def runTask(self, t = 'Blob2IO', processes = 6, *args):
		print("goo.....")		
		# 开启一个全局的对列，用于下面存放图片ROWID 
		imgQueue = Queue()
		blob2OS = Blob2OS(processes = processes, *args) \
		    if t == 'Blob2IO' else Blob2DB(processes = processes, *args)
		allProcesses = []
		
		if processes == 0:
			processes = cpu_count()
	
		master = Process(target=blob2OS.master,args=(imgQueue,))
		master.start()
		allProcesses.append(master)
		
		if t == 'Blob2IO':
			recQueue = Queue()
			record = Process(target=blob2OS.recordBlobId,args=(recQueue,))
			record.start()
			allProcesses.append(record)			

			for i in range(processes):
				slave = Process(target=blob2OS.slave,args=(imgQueue, recQueue,))
				slave.start()
				allProcesses.append(slave)
		else:
			for i in range(processes):
				slave = Process(target=blob2OS.slave,args=(imgQueue,))
				slave.start()
				allProcesses.append(slave)
				
	
		for slave in allProcesses:
			slave.join()
	
		print("end.....")		
	
	
	def runBlob2IO(self, blobNameSpliter, blobNameColumn, filePath, processes):
		self.blobNameColumnIndexList = []
		blobIdSQLStr = self.reGenBlob2OSSQL(self.blobIdSQL, blobNameColumn, t = 'SQL1')
		blobSQLStr = self.reGenBlob2OSSQL(self.blobSQL, blobNameColumn, t = 'SQL2')
		self.runTask('Blob2IO', processes, 
		             self.sourceDBConnStr,
		             blobIdSQLStr,
		             blobSQLStr,
		             filePath,
		             self.blobNameColumnIndexList, 
		             blobNameSpliter)
		
	
	def runBlob2DB(self, mapColumnList, processes = 6):
		self.columnPositionList = []
		sourceTableColumn = []
		targetTableColumn = []
		for cm in mapColumnList:
			sColumn, tColumn = cm
			targetTableColumn.append(tColumn)
			sourceTableColumn.append(sColumn)

		blobIdSQL = self.reAssembleSQL(self.blobIdSQL, sourceTableColumn, t = 'SQL1')
		blobSQL = self.reAssembleSQL(self.blobSQL, sourceTableColumn, t = 'SQL2')
		
		blobInsertSQL = "insert /*+append*/ into " \
		    + self.targetTable + "("+ ','.join(targetTableColumn) +") values "
		
		print(self.columnPositionList)
		self.runTask('Blob2DB', processes,
		             self.sourceDBConnStr,
		             self.targetDBConnStr,
		             blobIdSQL,
		             blobSQL,
		             blobInsertSQL,
		             self.columnPositionList)
		
	
	def reGenBlob2OSSQL(self, sqlStr, blobNameColumn, t = 'SQL1'):
		sqlStr1, sqlStr2 = re.split('from', sqlStr, flags= re.I)
		columnList = re.sub('select', '', sqlStr1, count = 1, flags = re.I).strip(' ').split(',')
		sqlStr1 = None
		
		for c in columnList:
			column1 = re.split(' |as', c, flags = re.I)[-1]
			if t == 'SQL1':
				column1 = 'SQL1.' + column1
			else:
				column1 = 'SQL2.' + column1
				
			if blobNameColumn.count(column1) > 0:
				ind = blobNameColumn.index(column1)
				self.blobNameColumnIndexList.append(ind)
			else:
				self.blobNameColumnIndexList.append(-1)
		
			column2 = c.strip(' ').upper()
			if column2.endswith('IMAGEID') or column2.endswith('IMAGE'):
				sqlStr1 = 'select ' + c + ' , '

		if not sqlStr1:
			return

		for c in columnList:
			column3 = c.strip(' ').upper()
			if column3.endswith('IMAGEID') or column3.endswith('IMAGE'):
				continue
			sqlStr1 += c + ' , '
	
		sqlStr = sqlStr1.rstrip(', ') + ' from ' + sqlStr2
		
		print(sqlStr)
		
		return sqlStr
	
	
	def reAssembleSQL(self, sqlStr, sourceTableColumn, t = 'SQL1'):
		sqlStr1, sqlStr2 = re.split('from', sqlStr, flags= re.I)
		columnList = re.sub('select', '', sqlStr1, count = 1, flags = re.I).strip(' ').split(',')
		sqlStr1 = None
	
		#对SQL重新构造，把ImageId和Image放在SQL的首位
		for c in columnList:	
			column2 = c.strip(' ').upper()
			if column2.endswith('IMAGEID') or column2.endswith('IMAGE'):
				sqlStr1 = 'select ' + c + ' , '
	
		if not sqlStr1:
			return
	
		for c in columnList:
			column3 = c.strip(' ').upper()
			if column3.endswith('IMAGEID') or column3.endswith('IMAGE'):
				continue
			sqlStr1 += c + ' , '
	
		sqlStr = sqlStr1.rstrip(', ') + ' from ' + sqlStr2
		
		print(sqlStr)
		
		#生成列在输入时的位置顺序
		sqlStr1, sqlStr2 = re.split('from', sqlStr, flags= re.I)
		columnList = re.sub('select', '', sqlStr1, count = 1, flags = re.I).split(',')
	
		for c in columnList:
			column1 = re.split(' |as', c.strip(' '), flags = re.I)[-1]
			if t == 'SQL1':
				column1 = 'SQL1.' + column1
			else:
				column1 = 'SQL2.' + column1
	
			if sourceTableColumn.count(column1) > 0:
				ind = sourceTableColumn.index(column1)
				self.columnPositionList.append(ind)
			else:
				self.columnPositionList.append(-1)				
	
		return sqlStr
	
		
	
		
			
				
		
			
		
			
		
		
		
		
		
		
		
			
				
				
				
		
			