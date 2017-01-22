import cx_Oracle, os
from util import ParaPrase

#paraprase = ParaPrase.get()
#user = paraprase['DATABASE']['user']
#passwd = paraprase['DATABASE']['password']
#ipaddr = paraprase['DATABASE']['ipaddr']
#port = paraprase['DATABASE']['port']
#servername = paraprase['DATABASE']['servername']
#nls_lang = paraprase['DATABASE']['nls_lang']
#os.environ['NLS_LANG'] = nls_lang if nls_lang else 'AMERICAN_AMERICA.ZHS16GBK'

#_DBURL = user + '/' + passwd + '@' + ipaddr + ':' + port + '/' + servername


class DBConnection(object):

    def __init__(self, dbconn):
        self.dbconn = dbconn
        self.connection = ''
        self.cursor = ''
        
    def __enter__(self):
        return self

    def openConnection(self):
        try:
            #self.connection = cx_Oracle.connect(_DBURL)
            self.connection = cx_Oracle.connect(self.dbconn)
            self.cursor = self.connection.cursor()
        except:
            print("连接数据库失败!!!")
        else:
            print("成功连接数据库!!!")
        finally:
            return self.cursor
        

    def __exit__(self, type, value, trace):
        print("退出数据库连接.")
        self.cursor.close()
        self.connection.close()        

if __name__ == "__main__":
    with DBConnection() as db:
        db.openConnection()
    


