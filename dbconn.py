# -*- coding: utf-8 -*-
import cx_Oracle

class DBConnection(object):
    def __init__(self, dbconn):
        self.dbconn = dbconn
        self.connection = ''
        self.cursor = None
        
    def __enter__(self):
        return self

    def openConnection(self):
        try:
            self.connection = cx_Oracle.connect(self.dbconn)
            self.cursor = self.connection.cursor()
        except Exception, e:
            print(u"连接数据库失败!!!")

        return self.cursor

    def __exit__(self, type, value, trace):
        if self.cursor:
            self.cursor.close()
            self.connection.close()        

if __name__ == "__main__":
    with DBConnection('system/oracle@orcl') as db:
        cursor = db.openConnection()
        cursor.execute("select * from v$session")
        
        


