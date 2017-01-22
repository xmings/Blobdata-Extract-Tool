import cx_Oracle, time, os
from dbconn import DBConnection
from util import WriteFile, ReadFile, ToolBox
from model import MutiThreadReadLog
"""
图片导入导出模块
导出时多个列可以使用||连接作为图片名字;导入时图片名字导入一个列中,然后用户可以数据库中拆分数据
"""

_PRECOMMIT = 500


class DBImport(MutiThreadReadLog):
    def __init__(self, parent, dbconn, table, piccolumn, picnamecolumn, picnamespliter, logfile):
        super(DBImport, self).__init__(parent, logfile, thread1=self.run, thread2=self.readLog)
        self.dbconn = dbconn
        self.table = table
        self.piccolumn = piccolumn
        self.picnamecolumn = picnamecolumn
        self.picnamespliter = picnamespliter
        self.logfile = logfile
        self.initsql();
        
    def initsql(self):
        if self.table.strip(' ').find(' ') > 0:
            raise Exception('数据只能导入到某个具体的表')

        self.sqlstr = "insert /*+APPEND(a)*/ into "+ self.table +" a ("+ self.picnamecolumn +"," \
            + self.piccolumn + ") values (" + ("'%s'," * len(self.picnamecolumn.split(','))).strip(',') + ",:blobData)"
        print(self.sqlstr)

    def run(self):
        reader = ReadFile(os.path.dirname(self.logfile))
        with DBConnection(self.dbconn) as dbConnection:
            self.cursor = dbConnection.openConnection()
            for fid, picname, pic in reader.scanpics():
                self.cursor.setinputsizes(blobData=cx_Oracle.BLOB)
                sqlstr = self.sqlstr% tuple(picname.split(self.picnamespliter))
                self.cursor.execute(sqlstr, {'blobData':pic})
                if fid % _PRECOMMIT == 0:
                    self.cursor.execute('commit')
                
            self.cursor.execute('commit')
                                

class DBExport(MutiThreadReadLog):
    def __init__(self, parent, dbconn, sqltext, piccolumn, picnamecolumn, picnamespliter, logfile):
        super(DBExport, self).__init__(parent, logfile, thread1=self.run)
        self.dbconn = dbconn
        self.sqltext = sqltext
        self.piccolumn = piccolumn
        self.picnamecolumn = picnamecolumn
        self.picnamespliter = picnamespliter
        self.logfile = logfile        
        self.initsql()
        
        
    def initsql(self):
        self.sqlstr = 'select rownum,' + self.picnamecolumn.replace(',', '||\''+self.picnamespliter+'\'||') \
            + ',' + self.piccolumn + ' from ' + self.sqltext
        print(self.sqlstr)

    def run(self):
        writer = WriteFile(os.path.dirname(self.logfile))
        if os.path.exists(self.logfile):
            os.remove(self.logfile)
            ToolBox.recordnumber(self.logfile, 0)
        with DBConnection(self.dbconn) as dbConnection:
            self.cursor = dbConnection.openConnection()
            try:
                self.cursor.execute(self.sqlstr)
                for res in self.cursor:
                    data = res[2].read() if res[2] else b''
                    filename = res[1] + '.jpg'
                    writer.writepic(filename, data, t='pic')
                    
                    if res[0] % _PRECOMMIT == 0:
                        ToolBox.recordnumber(self.logfile, res[0])
                
                ToolBox.recordnumber(self.logfile, str(self.cursor.rowcount))
                
            except Exception as e:
                return self.parent.displaylog("导出图片时异常：", e.args)
                
                

if __name__ == '__main__':
    dbimport = DBImport()
    dbimport.run()
