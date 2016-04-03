#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<wangms>
  Purpose:  --make the sqluldr2 better use than before
  Created: 2016-4-2
"""
import Tkinter as TK
import tkFileDialog
import model, os, cx_Oracle

class view(object):
    
    def __init__(self):
        self.root = TK.Tk(screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None)
        self.root.title(u"EAL工具")
        #self.root.geometry('600x300')                 #长x宽,是x 不是*
        self.root.resizable(width=False, height=False) #宽不可变, 高可变,默认为True
        
        
        #布局分上、中、下三块
        self.frm = TK.Frame(self.root)
        self.frm_t = TK.Frame(self.frm, bd=3)  #frm_t即top
        
        
        #上
        self.frm_up = TK.Frame(self.frm_t, bd=5)
        self.labelframe_up = TK.LabelFrame(self.frm_up, text = u"选项")
        
        #ORACLE源端连接
        self.conn_str1 = TK.StringVar(master=None, value=None, name=None)  
        TK.Label(self.labelframe_up, text = u'ORACLE源端连接:', font =('Consolas',10)).grid(row=0, column=0, sticky='w')
        self.dbentry1 = TK.Entry(self.labelframe_up, textvariable=self.conn_str1, width = 20, font =('con', 10))        
        self.dbentry1.grid(row=0, column=1, sticky='w')
                
        #列分隔符
        self.sepa_str = TK.StringVar(master=None, value=None, name=None)  
        TK.Label(self.labelframe_up, text = u'行分隔符:', font =('Consolas',10)).grid(row=0, column=2)
        self.sepaentry = TK.Entry(self.labelframe_up, textvariable=self.sepa_str, width = 10, font =('Consolas', 10))
        self.sepaentry.grid(row=0, column=3, sticky='w')
        
        #是否为BLOB
        self.is_blob = TK.IntVar()
        self.blobbutton = TK.Checkbutton(self.labelframe_up, text = u"是否BLOB", variable = self.is_blob, font =('Consolas',10), \
                                         onvalue = 1, offvalue = 0)
        self.blobbutton.grid(row=0, column=4)
        
        #ORACLE目标连接
        self.conn_str2 = TK.StringVar(master=None, value=None, name=None)  
        TK.Label(self.labelframe_up, text = u'ORACLE目标连接:', font =('Consolas',10)).grid(row=1, column=0, sticky='w')
        self.dbentry2 = TK.Entry(self.labelframe_up, textvariable=self.conn_str2, width = 20, font =('con', 10))        
        self.dbentry2.grid(row=1, column=1, sticky='w')
        
        #目标表
        self.imptab_str = TK.StringVar(master=None, value=u"目标表...", name=None)
        self.imptabentry = TK.Entry(self.labelframe_up, textvariable=self.imptab_str, width = 20, font =('con', 10))
        self.imptabentry.grid(row=1, column=2, sticky='w')
        
        #导入方式
        self.impmethod_int = TK.IntVar(master=None, value=0, name=None)
        self.impmethodbutton = TK.Radiobutton(self.labelframe_up, text="APPEND", variable=self.impmethod_int, \
                                              value=1).grid(row=1, column=3, sticky='w')
        self.impmethodbutton = TK.Radiobutton(self.labelframe_up, text="INSERT", variable=self.impmethod_int, \
                                              value=2).grid(row=1, column=4, sticky='w')
        
        
        
        #SQL语句
        self.sqltext = TK.Text(self.labelframe_up, height=4, width=72)
        self.sqltext.grid(row=2, column=0, columnspan=4, rowspan=2)
        self.sqltext.insert(TK.INSERT, u"输入SQL查询语句...")
        
        
        #执行
        self.execbutton = TK.Button(self.labelframe_up, text=u"执行", font =('Consolas',12), width=8)
        self.execbutton.bind('<Button-1>', self.exec_programe)
        self.execbutton.grid(row=2,column=4, sticky='s')
             

        self.labelframe_up.grid(sticky ='wn')
        self.frm_up.grid(row=0, column=0, sticky ='wn')
        
        
        #print self.labelframe_up.grid_size()
        #print self.labelframe_up.winfo_geometry()
        #print self.root.geometry()
        #print self.labelframe_up.size()
        #print self.labelframe_up.winfo_pointerxy() #窗口的绝对位置
        #print self.labelframe_up.winfo_x(), self.labelframe_up.winfo_y()
        #print self.labelframe_up.winfo_vrootheight(), self.labelframe_up.winfo_vrootwidth()  #屏幕的分变率
        #print self.labelframe_up.winfo_vrootx(), self.labelframe_up.winfo_vrooty()
        #print self.labelframe_up.winfo_width(), self.labelframe_up.winfo_height()  #
        
        
        
        #中
        self.frm_center = TK.Frame(self.frm_t, bd=5)
        self.labelframe_center = TK.LabelFrame(self.frm_center, text = u"输出")
        
        self.databutton = TK.Button(self.labelframe_center, text=u"数据文件路径", font =('Consolas', 9), width = 15)
        self.databutton.bind('<Button-1>', self.get_datafile)
        self.databutton.grid(row=0,column=0)
        self.datalabel = TK.Label(self.labelframe_center, text = u'....', font =('Consolas',10), width = 70, justify=TK.LEFT)
        self.datalabel.grid(row=0, column=1, columnspan=5, sticky='w')
        
        self.logbutton = TK.Button(self.labelframe_center, text=u"日志文件路径", font =('Consolas', 9), width = 15)
        self.logbutton.bind('<Button-1>', self.get_logfile)
        self.logbutton.grid(row=1,column=0)
        self.loglabel = TK.Label(self.labelframe_center, text = u'....', font =('Consolas',10), width = 70, justify=TK.LEFT)
        self.loglabel.grid(row=1, column=1, columnspan=5, sticky='w')
        
        self.ctlbutton = TK.Button(self.labelframe_center, text=u"控制文件路径", font =('Consolas', 9), width = 15)
        self.ctlbutton.bind('<Button-1>', self.get_ctlfile)
        self.ctlbutton.grid(row=2,column=0)
        self.ctllabel = TK.Label(self.labelframe_center, text = u'....', font =('Consolas',10), width = 70, justify=TK.LEFT)
        self.ctllabel.grid(row=2, column=1, columnspan=5, sticky='w')
                
             
        self.labelframe_center.grid(row=1, column=0,sticky='wn', columnspan=5)
        self.frm_center.grid(row=1, column=0, sticky='wn', columnspan=5)        
        
        self.frm_t.grid(sticky='nw')   
        
        
        #self.separator = TK.Frame(self.frm, heigh=2, bd=1, relief=TK.SUNKEN)
        #self.separator.pack(fill=TK.X, padx=5, pady=5)
        
        #m = TK.PanedWindow(orient=TK.VERTICAL)  
        #m.pack(fill=TK.BOTH, expand=1)
        
        #TK.PanedWindow(self.frm, bd=200, height=2, relief=TK.RAISED).grid(row=3, column=0, columnspan=3)
        
        #winfo_reqheight winfo_reqwidth 动态改变控件的大小和位置
          
        #底部
        self.frm_b = TK.Frame(self.frm, bd=3)  #frm_b即below
        self.labelframe_b = TK.LabelFrame(self.frm_b)
        self.logtext = TK.Text(self.labelframe_b, selectborderwidth=10, width=88)
        self.logtext.grid(sticky='w')
        self.labelframe_b.grid()
        self.frm_b.grid(sticky='w')
        
        self.frm.grid()
        
        
    def get_filename(self):
        filename = tkFileDialog.askopenfilename(initialdir = u'd:\\')
        return filename
    
    def get_datafile(self, event):
        self.datalabel['text'] = self.get_filename()
    
    def get_logfile(self, event):
        self.loglabel['text'] = self.get_filename()
    
    def get_ctlfile(self, event):
        print self.ctllabel['text']
        self.ctllabel['text'] = self.get_filename()
        
        
    def exec_programe(self, event):
        
        self.intejudge = False  #默认不加载数据
        
        if not self.sepa_str.get():
            self.sepastr = ';;;'
            self.sepa_str.set(self.sepastr)
        else:
            self.sepastr = self.sepa_str.get()
        
        if self.datalabel['text'] == '....' :
            self.datafile = os.path.join(model.curr_dir, 'expdatafile.txt')
            self.datalabel['text'] = self.datafile
    
        if self.loglabel['text'] == '....':
            self.logfile = os.path.join(model.curr_dir, 'explogfile.log')
            self.loglabel['text'] = self.logfile
        
        self.ctlfile = None if self.ctllabel['text'] == '....' else self.ctllabel['text'] 
                                                                                   
        try:
            if not self.conn_str1.get() or not self.sqltext.get('0.0', TK.END):
                raise ValueIsNull(u"数据库连接串和SQL查询语句必填！！")
            else:
                DBconnectCheck(self, self.conn_str1.get())
                if 'select' not in self.sqltext.get('0.0', TK.END) or 'from' not in self.sqltext.get('0.0', TK.END):
                    raise ValueIsNull(u"SQL语句不规范")
                
                
            if self.ctllabel and self.conn_str2.get() and self.imptab_str.get():
                self.intejudge = True
                DBconnectCheck(self, self.conn_str2.get())
                if not self.impmethod_int.get():
                    raise ValueIsNull(u"请选择数据导入方式")     
                                
        except ValueIsNull, e:
            self.logtext.insert(TK.END, ''.join(e.args)+'\n') 
            print e.args
        
        except:
            pass

        else:
            try:
                self.extract = model.ExtractData(self, \
                                                 self.conn_str1.get(), \
                                                 self.sqltext.get('0.0', TK.END), \
                                                 self.sepastr, \
                                                 self.datafile, \
                                                 self.logfile, \
                                                 self.ctlfile, \
                                                 self.imptab_str.get(), \
                                                 self.impmethod_int.get(), \
                                                 self.is_blob.get())
                self.extract.run()
                
            except Exception, e:
                self.logtext.insert(TK.END, u'抽取数据过程异常：'+'\n'+e.message+'\n')
                
            else:
                if self.intejudge:
                    try:
                        self.load = model.load(self, \
                                               self.conn_str2, \
                                               self.ctlfile)
                        self.load.run()
                    except Exception, e:
                        self.logtext.insert(TK.END, u'加载数据过程异常：'+'\n'+e.message+'\n')
    
class DBconnectCheck(object):
    def __init__(self, parent, connstr):
        self.parent = parent
        self.connstr = connstr
              
        try:
            if self.connstr.rfind('@') == -1:
                raise DBConnectError(u"数据库连接串异常")
            else:
                self.prestr = self.connstr[0:self.connstr.rfind('@')]
                self.poststr = self.connstr[self.connstr.rfind('@')+1:len(self.connstr)]
                
            if self.prestr.find('/') == -1:
                raise DBConnectError(u'用户名或密码错误')
            else:
                self.username = self.prestr[0:self.prestr.find('/')]
                self.password = self.prestr[self.prestr.find('/')+1:len(self.prestr)]
            
            if self.poststr.find('/') == -1:
                self.servip = self.poststr[0:self.poststr.find('/')]
                self.oraclesid = self.poststr[self.poststr.find('/')+1:len(self.poststr)]            
            
            
            cx_Oracle.connect(self.username, self.password, self.poststr)
            
        except DBConnectError, e:
            self.parent.logtext.insert(TK.END, ''.join(e.args)+'\n')  #e.args为数组，必须转为字符
            print e.args
        except:
            self.parent.logtext.insert('0.0', u'连接数据失败')
            print u'连接数据失败'
        
        
 
class ValueIsNull(RuntimeError):
    def __init__(self, args):
        self.args = args
                
class DBConnectError(RuntimeError):
    def __init__(self, args):
        self.args = args
      
                    
def run():
    v = view()
    v.root.mainloop()

if __name__ == '__main__':
    run()