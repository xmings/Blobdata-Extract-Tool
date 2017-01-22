import os
from util import ToolBox
from model import MutiThreadReadLog
from dbconn import DBConnection

"""
数据导入导出模块，不包含导图片功能
该功能引用了著名的sqluldr，以提高效率
"""
        
class DBImport(MutiThreadReadLog):
    def __init__(self, parent, dbconn, table, rowspliter, colspliter, controlfile, logfile, **args):
        self.parent = parent
        self.userid = dbconn
        self.table = table
        self.rowspliter = rowspliter
        self.colspliter = colspliter
        self.controlfile = controlfile
        self.logfile = logfile
        self.badfile = os.path.join(os.path.dirname(logfile), 'badfile.txt')
        
        super(DBImport, self).__init__(self.parent, self.logfile, thread1=self.run, thread2=self.readLog)
        
    def run(self):
        self.option = ' userid=' + self.userid \
            + ' control=' + self.controlfile \
            + ' log=' + self.logfile \
            + ' bad=' + self.badfile \
            + ' skip=100' \
            + ' errors=100'  \
            + ' multithreading=True' \
            + ' direct=TRUE'
        command = 'sqlldr' +' '+self.option.replace('\n', '')
        
        print(self.get_schema("SCOTT", "EMP"))
        try:
            os.system(command)
        except Exception as e:
            self.parent.displaylog("导出数据异常：", e)
            
            
    def get_schema(self, owner, table):
        sqlstr = "SELECT '\"'||COLUMN_NAME||'\"'||CHR(9)||DATA_TYPE||'('||DATA_LENGTH|| " + \
            "CASE WHEN A.DATA_PRECISION IS NOT NULL THEN ','||A.DATA_PRECISION||')' " + \
            "  ELSE ')'" + \
            " END ||' NULLIF  \"'||A.COLUMN_NAME||'\"=BLANKS,' AS COL" + \
            "FROM All_Tab_Cols A WHERE TABLE_NAME='EMP' OWNER=UPPER('"+ owner + "') AND TABLE_NAME=UPPER('" + table + "')"
        
        with DBConnection(self.userid) as dbconnection:
            self.cursor = dbConnection.openConnection()
            try:
                self.cursor.execute(sqlstr)
                return self.cursor.fetch()
            except Exception as e:
                return self.parent.displaylog("导出图片时异常：", e.args)
                    
        
        

class DBExport(MutiThreadReadLog):
    def __init__(self, parent, dbconn, query, field, record, datafile, \
                 logfile, ctlfile, imptable=None, impmethod=None, islob=None):
        self.parent = parent
        self.user = dbconn
        self.query = "' + query + '"
        self.field = field
        self.record = record
        self.datafile = datafile
        self.logfile = logfile
        self.ctlfile = ctlfile
              
        super(DBExport, self).__init__(self.parent, self.logfile, thread1=self.run, thread2=self.readLog)        

    def run(self):
        self.option = ' user=' + self.user \
            + ' query=' + self.query \
            + 'field=' + self.field \
            + 'record=' + self.record \
            + 'file=' + self.datafile \
            + 'log=' + self.logfile \
            + 'control' + self.ctlfile \
            +' table=TARGET_TABLENAME' \
            +' mode=INSERT' \
            +' degree=8'             
        try:
            command = ToolBox.get_sqluldr(self.parent) +' '+self.option.replace('\n', '')
            print(command)
            os.system(command)
        except Exception as e:
            self.parent.displaylog("导出数据异常：", e)