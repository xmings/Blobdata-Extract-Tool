import tkinter as TK
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
from control import MainControl

class MainUI(object):    
    def __init__(self):
        self.maincontrol = MainControl(self)
        self.root = TK.Tk(screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None)
        self.center_window(690, 620)
        self.root.title("DBIO--数据导入导出工具")
        self.root.iconbitmap("images/dao.ico")
        self.root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
        
        
        #布局分上、中、下三块
        self.frm = TK.Frame(self.root)
        
        #导数方式
        self.frm_up = TK.Frame(self.frm, bd=3)  #frm_t即top
        self.labelframe_up = TK.LabelFrame(self.frm_up, padx=10, pady=5, text = "导数方式")
        
        self.io_method = TK.StringVar(master=None, value=None, name=None)
        self.default_radiobutton = TK.Radiobutton(self.labelframe_up, variable=self.io_method, text='导入数据', value='idata', \
                                                  command=self.get_idata_label)
        self.default_radiobutton.grid(row=0, column=0, sticky='w')
        self.default_radiobutton.select()
        TK.Radiobutton(self.labelframe_up, variable=self.io_method, text='导出数据', value='odata', command=self.get_odata_label)\
            .grid(row=0, column=1, sticky='w')
        TK.Radiobutton(self.labelframe_up, variable=self.io_method, text='导入图片', value='ipic', command=self.get_ipic_label)\
            .grid(row=0, column=2, sticky='w')        
        TK.Radiobutton(self.labelframe_up, variable=self.io_method, text='导出图片', value='opic', command=self.get_opic_label)\
            .grid(row=0, column=3, sticky='w')
        
        
        # 执行按钮
        self.execbutton = TK.Button(self.labelframe_up, text="执行", font =('Consolas',12), width=8)
        self.execbutton.bind('<Button-1>', self.maincontrol.exec_programe)
        self.execbutton.grid(row=0,column=4, sticky='s', padx=15)
             
             
        #数据库选项
        self.labelframe_database = TK.LabelFrame(self.labelframe_up, text = "数据库选项", padx=10, pady=10)
          
        
        # ORACLE数据库连接
        self.dbconn_str = TK.StringVar(master=None, value=None, name=None)  
        TK.Label(self.labelframe_database, text = '数据库连接串:', font =('Consolas',10)).grid(row=0, column=0, sticky='w')
        self.dbconn_entry = TK.Entry(self.labelframe_database, textvariable=self.dbconn_str, width = 77, font =('Consolas', 10))
        self.dbconn_entry.grid(row=0, column=1, columnspan=5, sticky='w')

        
        # 字符集
        self.nlslang_str = TK.StringVar(master=None, value=None, name=None)  
        TK.Label(self.labelframe_database, text = '数据库字符集:', font =('Consolas',10)).grid(row=1, column=0, sticky='w')
        self.nlslang_entry = TK.Entry(self.labelframe_database, textvariable=self.nlslang_str, width = 77, font =('Consolas', 10))
        self.nlslang_entry.grid(row=1, column=2, columnspan=5, sticky='w')
        
        self.labelframe_database.grid(row=1, column=0,sticky='wn', columnspan=5)
        
        #数据选项
        self.generate_data_label()
        
        #文件选项
        self.labelframe_file = TK.LabelFrame(self.labelframe_up, \
                                             text = "文件选项--数据文件文件名为datafile.txt，控制文件文件为control.txt")
    
        # 数据文件或者图片文件路径
        self.iopath_button = TK.Button(self.labelframe_file, text="数据或图片目录", font =('Consolas', 9), width = 15)
        self.iopath_button.bind('<Button-1>', self.get_path)
        self.iopath_label = TK.Label(self.labelframe_file, font =('Consolas',10), width = 73, justify="left", anchor="w")
        self.iopath_button.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.iopath_label.grid(row=0, column=1, columnspan=5, sticky='w')
        self.labelframe_file.grid(row=3, column=0,sticky='wn', columnspan=5)          

        self.labelframe_up.grid(sticky ='wn')
        self.frm_up.grid(row=0, column=0, sticky ='wn')         

        #底部
        self.frm_down = TK.Frame(self.frm, bd=3)  #frm_b即below
        self.labelframe_b = TK.LabelFrame(self.frm_down)
        
        self.logtext = ScrolledText(self.labelframe_b, selectborderwidth=10, width=94, wrap=TK.WORD)        
        self.logtext.grid(row=0, column=0, sticky ='wn')    
    
        self.labelframe_b.grid(sticky='wn')
        self.frm_down.grid(row=1, column=0, sticky ='wn')

        
        self.get_idata_label()  
        self.frm.grid()            
        
    def generate_data_label(self):
        #数据选项
        self.labelframe_data = TK.LabelFrame(self.labelframe_up, text = "数据选项", padx=10, pady=10)
        
        #数据行分隔符
        self.rowspliter_str = TK.StringVar(master=None, value=None, name=None)  
        self.rowspliter_label = TK.Label(self.labelframe_data, text = '行分隔符:', font =('Consolas',10))
        self.rowspliter_entry = TK.Entry(self.labelframe_data, textvariable=self.rowspliter_str, width = 10, font =('Consolas', 10))
    
        #数据列分隔符
        self.colspliter_str = TK.StringVar(master=None, value=None, name=None)  
        self.colspliter_label = TK.Label(self.labelframe_data, text = '列分隔符:', font =('Consolas',10))
        self.colspliter_entry = TK.Entry(self.labelframe_data, textvariable=self.colspliter_str, width = 10, font =('Consolas', 10))
    
        #或图片名称分割符
        self.picnamespliter_str = TK.StringVar(master=None, value=None, name=None)  
        self.picnamespliter_label = TK.Label(self.labelframe_data, text = '图片名称分隔符:', font =('Consolas',10))
        self.picnamespliter_entry = TK.Entry(self.labelframe_data, textvariable=self.picnamespliter_str, width = 25, font =('Consolas', 10))        
        
        #表名
        self.table_str = TK.StringVar(master=None, value=None, name=None)  
        self.table_label = TK.Label(self.labelframe_data, text = '导入到表：', font =('Consolas',10))
        self.table_entry = TK.Entry(self.labelframe_data, textvariable=self.table_str, width = 80, font =('Consolas', 10))
    
        #SQL语句
        self.sqltext_label = TK.Label(self.labelframe_data, text = '需要导出数据的SQL语句:', font =('Consolas',10))
        self.sqltext = TK.Text(self.labelframe_data, height=8, width=90)              

        #导入导出图片信息
        #图片列
        self.piccolumn_str = TK.StringVar(master=None, value=None, name=None)  
        self.piccolumn_label = TK.Label(self.labelframe_data, text = '图片列：', font =('Consolas',10))
        self.piccolumn_entry = TK.Entry(self.labelframe_data, textvariable=self.piccolumn_str, width = 30, font =('Consolas', 10))
    
    
        #图片名称列
        self.picnamecolumn_str = TK.StringVar(master=None, value=None, name=None)  
        self.picnamecolumn_label = TK.Label(self.labelframe_data, text = '图片名称列：', font =('Consolas',10))
        self.picnamecolumn_entry = TK.Entry(self.labelframe_data, textvariable=self.picnamecolumn_str, width = 78, font =('Consolas', 10))


    def get_idata_label(self):
        self.labelframe_data.destroy()
        self.generate_data_label()
        
        self.rowspliter_label.grid(row=0, column=0, sticky='w')
        self.rowspliter_entry.grid(row=0, column=1, sticky='w')
        self.colspliter_label.grid(row=0, column=2, sticky='w')
        self.colspliter_entry.grid(row=0, column=3, sticky='w')
        self.table_label.grid(row=3, column=0, sticky='w', pady=5)
        self.table_entry.grid(row=3, column=1, columnspan=4, sticky='w', pady=5)      
        
        self.labelframe_data.grid(row=2, column=0,sticky='wn', columnspan=5)
            
        
        self.maincontrol.renderpara()
           
        
    def get_odata_label(self):
        self.labelframe_data.destroy()
        self.generate_data_label()
        
        self.rowspliter_label.grid(row=0, column=0, sticky='w')
        self.rowspliter_entry.grid(row=0, column=1, sticky='w')
        self.colspliter_label.grid(row=0, column=2, sticky='w')
        self.colspliter_entry.grid(row=0, column=3, sticky='w')
        self.sqltext_label.grid(row=1, column=0, columnspan=4, sticky='w', pady=5)
        self.sqltext.grid(row=2, column=0, columnspan=4, sticky='w', pady=5)

        self.labelframe_data.grid(row=2, column=0,sticky='wn', columnspan=5)
        self.maincontrol.renderpara()
    
    def get_ipic_label(self):
        self.labelframe_data.destroy()
        self.generate_data_label()
        
        self.piccolumn_label.grid(row=0, column=0, sticky='w')
        self.piccolumn_entry.grid(row=0, column=1, sticky='w')        
        
        self.picnamespliter_label.grid(row=0, column=2, sticky='w')
        self.picnamespliter_entry.grid(row=0, column=3, sticky='w')
        
        self.picnamecolumn_label.grid(row=2, column=0, sticky='w')
        self.picnamecolumn_entry.grid(row=2, column=1, columnspan=4, sticky='w', pady=5)
        
        self.table_label.grid(row=3, column=0, sticky='w', pady=5)
        self.table_entry.config(width=78)
        self.table_entry.grid(row=3, column=1, columnspan=4, sticky='w', pady=5)

        self.labelframe_data.grid(row=2, column=0,sticky='wn', columnspan=5)
        self.maincontrol.renderpara()
        
    def get_opic_label(self):
        self.labelframe_data.destroy()
        self.generate_data_label()
        
        self.piccolumn_label.grid(row=0, column=0, sticky='w')
        self.piccolumn_entry.grid(row=0, column=1, sticky='w')        
        
        self.picnamespliter_label.grid(row=0, column=2, sticky='w')
        self.picnamespliter_entry.grid(row=0, column=3, sticky='w')
        
        self.picnamecolumn_label.grid(row=2, column=0, sticky='w')
        self.picnamecolumn_entry.grid(row=2, column=1, columnspan=4, sticky='w', pady=5)
        
        self.sqltext_label.grid(row=33, column=0, columnspan=4, sticky='w', pady=5)
        self.sqltext.grid(row=34, column=0, columnspan=4, sticky='w', pady=5)
            
        
        self.labelframe_data.grid(row=2, column=0,sticky='wn', columnspan=5)
        self.maincontrol.renderpara()

        
    def center_window(self, width, height):  
        screenwidth = self.root.winfo_screenwidth()  
        screenheight = self.root.winfo_screenheight()  
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  
        self.root.geometry(size)           
    def get_path(self, event):
        self.iopath_label['text'] = tkinter.filedialog.askdirectory(initialdir='d:\\')
        

if __name__ == '__main__':
    v = MainUI()
    v.root.mainloop()
    