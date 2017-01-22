import model, os, cx_Oracle
import tkinter as TK
from util import ParaPrase
from dataio import DBExport as DataExport
from dataio import DBImport as DataImport
from picio import DBExport as PicExport
from picio import DBImport as PicImport


class MainControl(object):
    
    def __init__(self, parent):
        self.parent = parent
    
    def exec_programe(self, event):        
        if not self.parent.dbconn_str.get() or not self.parent.nlslang_str.get() or not self.parent.iopath_label['text']:
            return self.displaylog('请填写所有选项！！')
            
        self.dbconn_str = self.parent.dbconn_str.get()
        self.nlslang_str = self.parent.nlslang_str.get()
        self.iopath_str = self.parent.iopath_label['text']
        os.environ['NLS_LANG'] = self.nlslang_str
        self.datafile = os.path.join(self.iopath_str, 'datafile.txt')
        self.logfile = os.path.join(self.iopath_str, 'logfile.log')
        self.ctlfile = os.path.join(self.iopath_str, 'controlfile.txt')
        

        if self.parent.io_method.get() in ('odata', 'iodata'):
            if not self.parent.rowspliter_str.get() or not self.parent.colspliter_str.get():
                return self.displaylog('请填写所有选项！！')

            self.rowspliter_str = self.parent.rowspliter_str.get()
            self.colspliter_str = self.parent.colspliter_str.get()

            
            if self.parent.io_method.get() == 'odata':
                if not self.parent.sqltext.get('0.0', TK.END):
                    return self.displaylog('请填写要导出数据的完整SQL语句！！')                  
                try:
                    dataexport = DataExport(self, self.dbconn_str, self.parent.sqltext.get('0.0', TK.END), \
                                            self.colspliter_str, self.rowspliter_str, \
                                            self.datafile, self.logfile, self.ctlfile)
                    dataexport.start()
                    ParaPrase.set('TABLE', 'exportsqlstr', self.parent.sqltext.get('0.0', TK.END))
                except Exception as e:
                    return self.displaylog('导出数据异常:', e.args)
                    
            else:
                if not self.parent.table_str.get():
                    return self.displaylog('请填写要导入的表！！')                  
                try:
                    dataimport = DataImport(self, self.dbconn_str, self.parent.table_str.get(), \
                                            self.rowspliter_str, self.colspliter_str, self.ctlfile, self.logfile)
                    dataimport.start()
                    ParaPrase.set('TABLE', 'importtable', self.parent.table_str.get())
                except Exception as e:
                    return self.displaylog('导入数据异常:', e.args)
                
            ParaPrase.set('DATA', 'rowspliter', self.rowspliter_str)
            ParaPrase.set('DATA', 'colspliter', self.colspliter_str)              

        else:
            if not self.parent.piccolumn_str.get() or not self.parent.picnamecolumn_str.get() \
               or not self.parent.picnamespliter_str.get():
                return self.displaylog('请填写所有选项！！')
            self.piccolumn = self.parent.piccolumn_str.get()
            self.picnamecolumn = self.parent.picnamecolumn_str.get()
            self.picnamespliter = self.parent.picnamespliter_str.get()
            
            if self.parent.io_method.get() == 'ipic':
                if not self.parent.table_str.get():
                    return self.displaylog('请填写要导入的表！！')
                try:
                    picimport = PicImport(self, self.dbconn_str, self.parent.table_str.get(), \
                                          self.piccolumn, self.picnamecolumn, self.picnamespliter, self.logfile)
                    picimport.start()
                    ParaPrase.set('TABLE', 'importtable', self.parent.table_str.get())
                except Exception as e:
                    return self.displaylog('导入图片异常:', e.args)                  
                
                
            else:
                if not self.parent.sqltext.get('0.0', TK.END):
                    return self.displaylog('请填写要导出数据的SQL语句，注意只需要FROM以及后面的部分！！')  
                try:
                    picexport = PicExport(self, self.dbconn_str, self.parent.sqltext.get('0.0', TK.END), \
                                          self.piccolumn, self.picnamecolumn, self.picnamespliter, self.logfile)
                    picexport.start()
                    ParaPrase.set('TABLE', 'exportsqlstr', self.parent.sqltext.get('0.0', TK.END))
                except Exception as e:
                    return self.displaylog('导出图片异常:', e.args)
                
            ParaPrase.set('PICTURE', 'piccolumn', self.piccolumn)
            ParaPrase.set('PICTURE', 'picnamecolumn', self.picnamecolumn)
            ParaPrase.set('PICTURE', 'picnamespliter', self.picnamespliter)  

                    
        ParaPrase.set('DATABASE', 'dbconn', self.dbconn_str)
        ParaPrase.set('DATABASE', 'nls_lang', self.nlslang_str)
                      
        
    def renderpara(self):
        self.parent.dbconn_entry.delete('0', 'end')
        self.parent.dbconn_entry.insert('0', ParaPrase.get_other('DATABASE', 'dbconn'))
        self.parent.rowspliter_entry.delete('0', 'end')
        self.parent.rowspliter_entry.insert('0', ParaPrase.get_spliter('rowspliter'))
        self.parent.colspliter_entry.delete('0', 'end')
        self.parent.colspliter_entry.insert('0', ParaPrase.get_spliter('colspliter'))
        self.parent.nlslang_entry.delete('0', 'end')
        self.parent.nlslang_entry.insert('0', ParaPrase.get_other('DATABASE', 'nls_lang'))
        self.parent.table_entry.delete('0', 'end')
        self.parent.table_entry.insert('0', ParaPrase.get_other('TABLE', 'importtable'))
        self.parent.piccolumn_entry.delete('0', 'end')
        self.parent.piccolumn_entry.insert('0', ParaPrase.get_other('PICTURE', 'piccolumn'))        
        self.parent.picnamecolumn_entry.delete('0', 'end')
        self.parent.picnamecolumn_entry.insert('0', ParaPrase.get_other('PICTURE', 'picnamecolumn'))
        self.parent.picnamespliter_entry.delete('0', 'end')
        self.parent.picnamespliter_entry.insert('0', ParaPrase.get_other('PICTURE', 'picnamespliter'))          
        self.parent.sqltext.delete(0.0,TK.END)
        self.parent.sqltext.insert('0.0', ParaPrase.get_other('TABLE', 'exportsqlstr'))
        self.parent.iopath_label['text'] = ParaPrase.get_other('FILE', 'iopath')
        

    def displaylog(self, tips, info=''):
        if tips and not tips.endswith('\n'):
            tips += '\n'
        elif not tips:
            return
        
        if not isinstance(info, list) and not isinstance(info, tuple):            
            text = tips + '\n'.join(info)
        elif info:
            text = tips + info
        else:
            text = tips
            
        # 如何在insert时控制字体颜色？    
        self.parent.logtext.insert(TK.END, text)
            