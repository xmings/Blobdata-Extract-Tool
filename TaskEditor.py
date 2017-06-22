# -*- coding: utf-8 -*-
import sys, os, time
from Control import Control
from PyQt4 import QtGui, QtCore, Qt


class TaskEditor(QtGui.QWidget):
    def __init__(self, parent=None, flags=0):
        super(TaskEditor, self).__init__(parent=None)
        self.setWindowTitle(u"BLOB Data Extract Tool")
        self.setWindowIcon(QtGui.QIcon('./beng1.ico'))
        self.globalLayout = QtGui.QGridLayout()
        self.setLayout(self.globalLayout)
        self.setMinimumSize(500, 700)
        self.globalLayout.setVerticalSpacing(4)
        self.globalLayout.setHorizontalSpacing(4)		
        self.globalLayout.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignLeft)
        self.setWindowFlags(Qt.Qt.WindowStaysOnTopHint)

        self.dbConnStatus = False
        self.chooseColumnStatus = False
        self.control = Control()
        self.initUI()

    def initUI(self):
        #数据源
        sourceDBLabel = QtGui.QLabel(u'数据源连接:')
        sourceDBLabel.setFixedWidth(80)
        self.sourceDBText = QtGui.QLineEdit('system/oracle@orcl')
        self.sourceDBText.setMinimumWidth(280)
        self.sourceDBTestButton = QtGui.QPushButton(u'1.测试数据连接')
        self.sourceDBTestButton.clicked.connect(self.on_sourceDBTestButton_clicked)
        self.sourceDBTestLabel = QtGui.QLabel()
        self.sourceDBTestLabel.setFixedHeight(20)

        self.globalLayout.addWidget(sourceDBLabel, 0, 0, 1, 1)
        self.globalLayout.addWidget(self.sourceDBText, 0, 1, 1, 1)
        self.globalLayout.addWidget(self.sourceDBTestButton, 0, 2, 1, 1)
        self.globalLayout.addWidget(self.sourceDBTestLabel, 1, 1, 1, 2)


        #SQL区域
        self.blobIdSQLGroupBox = QtGui.QGroupBox(u"SQL1:填写获取需要抽取的图片的图片ID及其它列的SQL")
        blobIdSQLTipsLabel = QtGui.QLabel(u"图片ID列请指定别名为ImageId;其它列名也最好使用别名,以便程序识别,以下同理。")
        blobIdSQLTipsLabel.setStyleSheet('''QLabel{color:red}''')
        self.blobIdSQLLayout = QtGui.QVBoxLayout()
        self.blobIdSQLGroupBox.setLayout(self.blobIdSQLLayout)
        self.blobIdSQLEditor = QtGui.QTextEdit("select imageid as ImageId,xm from test_base")
        self.blobIdSQLEditor.setFixedHeight(60)
        self.blobIdSQLLayout.addWidget(blobIdSQLTipsLabel, 0, Qt.Qt.AlignTop)
        self.blobIdSQLLayout.addWidget(self.blobIdSQLEditor, 1, Qt.Qt.AlignTop)
        self.globalLayout.addWidget(self.blobIdSQLGroupBox, 2, 0, 1, 3, Qt.Qt.AlignTop)


        self.blobSQLGroupBox = QtGui.QGroupBox(u"SQL2:填写通过图片ID获取唯一图片及其它列的SQL")
        blobSQLTipsLabel = QtGui.QLabel(u"图片列请指定别名Image;同时条件中的图片ID的值请使用'%s'指定,如Where ImageId='%s'。")
        blobSQLTipsLabel.setStyleSheet('''QLabel{color:red}''')
        self.blobSQLLayout = QtGui.QVBoxLayout()
        self.blobSQLGroupBox.setLayout(self.blobSQLLayout)
        self.blobSQLEditor = QtGui.QTextEdit("SELECT zp as Image,sfzhm FROM test_image where imageid='%s'")
        self.blobSQLEditor.setFixedHeight(60)
        self.blobSQLLayout.addWidget(blobSQLTipsLabel, 0, Qt.Qt.AlignTop)
        self.blobSQLLayout.addWidget(self.blobSQLEditor, 1, Qt.Qt.AlignTop)
        self.globalLayout.addWidget(self.blobSQLGroupBox, 3, 0, 1, 3, Qt.Qt.AlignTop)		


        processesLabel = QtGui.QLabel(u"并发进程数：")
        self.processesEditor = QtGui.QLineEdit('6')
        #processesValidator = QtGui.QRegExpValidator(Qt.QRegExp('[0-9]+'))
        self.processesEditor.setValidator(QtGui.QIntValidator(1, 64))

        self.processesEditor.setFixedWidth(110)
        self.sourceTableColumnButton = QtGui.QPushButton(u"2.获取源数据所有列")
        self.sourceTableColumnButton.setEnabled(False)
        self.sourceTableColumnButton.clicked.connect(self.on_sourceTableColumnButton_clicked)
        self.globalLayout.addWidget(processesLabel, 4, 0, 1, 1)
        self.globalLayout.addWidget(self.processesEditor, 4, 1, 1, 1)
        self.globalLayout.addWidget(self.sourceTableColumnButton, 4, 2, 1, 1)

        """选择抽取图片到文件系统还是数据库"""
        self.extractMethodTab = QtGui.QTabWidget()
        self.initBlob2IOTab()
        self.initBlob2DBTab()
        self.globalLayout.addWidget(self.extractMethodTab, 5, 0, 1, 3)

    def initBlob2IOTab(self):
        #第一个TAB页
        self.blob2IOWidget = QtGui.QWidget()
        self.blob2IOLayout = QtGui.QGridLayout()
        self.blob2IOLayout.setVerticalSpacing(20)
        self.blob2IOLayout.setAlignment(Qt.Qt.AlignLeft | Qt.Qt.AlignTop)
        self.blob2IOWidget.setLayout(self.blob2IOLayout)

        #指定图片名称组成列
        blobNameSplitLabel = QtGui.QLabel(u'3.指定图片名分割符：')
        self.blobNameSplitText = QtGui.QLineEdit(u'_')
        self.blobNameSplitText.setFixedWidth(110)
        blobNameColumnLabel = QtGui.QLabel(u'4.指定图片名称列：')
        self.blob2IOLayout.addWidget(blobNameSplitLabel, 0, 0, 1, 1)
        self.blob2IOLayout.addWidget(self.blobNameSplitText, 0, 1, 1, 2)
        self.blob2IOLayout.addWidget(blobNameColumnLabel, 1, 0, 1, 1) 		

        #图片输出位置
        self.ioPathEdit = Qt.QLineEdit("e:\\")
        self.ioPathEdit.setFixedWidth(340)
        self.ioPathEdit.setEnabled(False)
        ioPathButton = Qt.QPushButton(u'5.选择图片输出目录')
        ioPathButton.clicked.connect(self.on_ioPathButton_clicked)
        self.blob2IOLayout.addWidget(ioPathButton, 7, 0, 1, 1)
        self.blob2IOLayout.addWidget(self.ioPathEdit, 7, 1, 1, 3)


        self.runButton1 = QtGui.QPushButton(u"任务开始")
        self.runButton1.setEnabled(False)
        self.runButton1.setObjectName('run1')
        self.runButton1.setFixedSize(110, 40)
        self.runButton1.setStyleSheet('''QPushButton{font-size:12px;font-weight:bold}''')
        self.runButton1.clicked.connect(self.on_runButton_clicked)
        self.blob2IOLayout.addWidget(self.runButton1, 8, 3, 1, 1, Qt.Qt.AlignBottom)


        self.extractMethodTab.addTab(self.blob2IOWidget, u'抽取图片到文件系统')


    def initBlob2DBTab(self):
        self.blob2DBWidget = QtGui.QWidget()
        blob2DBLayout = QtGui.QGridLayout()
        blob2DBLayout.setAlignment(Qt.Qt.AlignLeft | Qt.Qt.AlignTop)
        self.blob2DBWidget.setLayout(blob2DBLayout)

        #目标源
        targetDBLabel = QtGui.QLabel(u'目标库连接:')
        targetDBLabel.setFixedWidth(80)
        self.targetDBText = QtGui.QLineEdit('system/oracle@orcl')
        self.targetDBText.setMinimumWidth(280)
        self.targetDBTestButton = QtGui.QPushButton(u'3、测试目标库连接')
        self.targetDBTestButton.clicked.connect(self.on_targetDBTestButton_clicked)
        self.targetDBTestLabel = QtGui.QLabel()
        self.targetDBTestLabel.setFixedHeight(20)
        blob2DBLayout.addWidget(targetDBLabel, 0, 0, 1, 1)
        blob2DBLayout.addWidget(self.targetDBText, 0, 1, 1, 1)
        blob2DBLayout.addWidget(self.targetDBTestButton, 0, 2, 1, 1)
        blob2DBLayout.addWidget(self.targetDBTestLabel, 1, 1, 1, 2)

        self.extractMethodTab.addTab(self.blob2DBWidget, u'抽取图片到数据库')


        #目标表
        targetTableLabel = QtGui.QLabel(u'目标库表:')
        targetTableLabel.setFixedWidth(80)
        self.targetTableText = QtGui.QLineEdit('test_target')
        self.targetTableText.setMinimumWidth(280)
        self.targetTableColumnButton = QtGui.QPushButton(u'4、获取目标表字段')
        self.targetTableColumnButton.setEnabled(False)
        self.targetTableColumnButton.clicked.connect(self.on_targetTableColumnButton_clicked)
        self.targetTableTestLabel = QtGui.QLabel()
        blob2DBLayout.addWidget(targetTableLabel, 2, 0, 1, 1)
        blob2DBLayout.addWidget(self.targetTableText, 2, 1, 1, 1)
        blob2DBLayout.addWidget(self.targetTableColumnButton, 2, 2, 1, 1)
        blob2DBLayout.addWidget(self.targetTableTestLabel, 3, 1, 1, 2)

        #映射列
        self.mapColumnWidget = QtGui.QGroupBox(u"源表列与目标列映射关系")
        self.mapColumnWidget.setMaximumWidth(365)
        self.mapColumnLayout = QtGui.QGridLayout()
        self.mapColumnLayout.setAlignment(Qt.Qt.AlignLeft | Qt.Qt.AlignCenter)
        self.mapColumnWidget.setLayout(self.mapColumnLayout)
        self.mapColumnLayout.addWidget(QtGui.QLabel(u'源表列'), 0, 0, 1, 1, Qt.Qt.AlignCenter)
        self.mapColumnLayout.addWidget(QtGui.QLabel(u'目标表列'), 0, 1, 1, 1, Qt.Qt.AlignCenter)
        self.mapColumnLayout.setColumnStretch(0, 1)
        self.mapColumnLayout.setColumnStretch(1, 1)
        blob2DBLayout.addWidget(self.mapColumnWidget, 4, 0, 3, 3)

        
        self.runButton2 = QtGui.QPushButton(u"任务开始")
        self.runButton2.setEnabled(False)
        self.runButton2.setObjectName('run2')
        self.runButton2.setFixedSize(110, 40)
        self.runButton2.setStyleSheet('''QPushButton{font-size:12px;font-weight:bold}''')
        self.runButton2.clicked.connect(self.on_runButton_clicked)
        self.mapColumnTipLabel = QtGui.QLabel()
        self.mapColumnTipLabel.setWordWrap(True)
        self.mapColumnTipLabel.setStyleSheet('''QLabel{color:red}''')
        blob2DBLayout.addWidget(self.runButton2, 4, 2, 1, 1, Qt.Qt.AlignTop)
        blob2DBLayout.addWidget(self.mapColumnTipLabel, 5, 2, 2, 1, Qt.Qt.AlignTop)


    def on_sourceDBTestButton_clicked(self):
        dbConnStr = self.sourceDBText.text()
        if not dbConnStr:
            return
        testResult = self.control.getDBConnStatus(str(dbConnStr))

        if testResult:
            self.dbConnStatus = True
            self.sourceDBTestLabel.setText(u"* 源数据库连接成功")
            self.sourceDBTestLabel.setStyleSheet('''QLabel{color:green}''')
            self.sourceTableColumnButton.setEnabled(True)
        else:
            self.dbConnStatus = False
            self.sourceDBTestLabel.setText(u"* 源数据库数据失败")
            self.sourceDBTestLabel.setStyleSheet('''QLabel{color:red}''')
            self.sourceTableColumnButton.setEnabled(False)


    def on_ioPathButton_clicked(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, u'选择图片输出目录', 'e:\\')
        if filename:
            self.ioPathEdit.setText(filename)

    def on_targetDBTestButton_clicked(self):
        dbConnStr = str(self.targetDBText.text())
        if not dbConnStr:
            return
        testResult = self.control.getDBConnStatus(dbConnStr, 'targetDB')


        if testResult:
            self.dbConnStatus = True
            self.targetDBTestLabel.setText(u"* 源数据库连接成功")
            self.targetDBTestLabel.setStyleSheet('''QLabel{color:green}''')
            self.targetTableColumnButton.setEnabled(True)
        else:
            self.dbConnStatus = False
            self.targetDBTestLabel.setText(u"* 源数据库连接失败")
            self.targetDBTestLabel.setStyleSheet('''QLabel{color:red}''')

    def on_targetTableColumnButton_clicked(self):
        tableName = str(self.targetTableText.text())
        if self.dbConnStatus:
            result = self.control.getTargetTableColumn(tableName)
            self.showMapColumnGrid(result, 'right')
            self.targetTableTestLabel.setText(u"* 获取列信息成功")
            self.targetTableTestLabel.setStyleSheet('''QLabel{color:green}''')
            self.runButton2.setEnabled(True)
        else:
            self.targetTableTestLabel.setText(u"* 获取列信息失败")
            self.targetTableTestLabel.setStyleSheet('''QLabel{color:red}''')



    def showMapColumnGrid(self, columnList, location = 'left'):
        for w in self.mapColumnWidget.findChildren(Qt.QWidget, Qt.QRegExp('.*' + location + '.*')):
            w.deleteLater()
        self.mapColumnWidget.update()
        
        if location == 'right':
            columnList.append('')

        for i in range(len(columnList) - 1):
            mapColumnComboBox = QtGui.QComboBox()
            mapColumnComboBox.setFixedSize(110, 20)
            mapColumnComboBox.setObjectName('mapColumnComboBox-' + location + '-' + str(i))
            for cName in columnList:
                mapColumnComboBox.addItem(Qt.QString(cName), Qt.QVariant(cName))
            if location == 'left':
                self.mapColumnLayout.addWidget(mapColumnComboBox, i + 1, 0, 1, 1, Qt.Qt.AlignCenter)
            else:
                self.mapColumnLayout.addWidget(mapColumnComboBox, i + 1, 1, 1, 1, Qt.Qt.AlignCenter)


    def on_sourceTableColumnButton_clicked(self):
        blobIdSQL = self.blobIdSQLEditor.toPlainText()
        blobSQL = self.blobSQLEditor.toPlainText()
        
        columnList = self.control.getSourceTableColumnName(str(blobIdSQL), str(blobSQL))
        columnList.append('')
        for w in self.blob2IOWidget.findChildren(Qt.QComboBox, Qt.QRegExp('blobNameColumnComboBox.*')):
            w.deleteLater()

        for i in range(len(columnList) - 2):
            blobNameColumnComboBox = QtGui.QComboBox()
            blobNameColumnComboBox.setFixedWidth(110)
            blobNameColumnComboBox.setObjectName("blobNameColumnComboBox-" + str(i + 1))
            
            for c in columnList:
                if c.endswith('.Image'):
                    continue
                blobNameColumnComboBox.addItem(Qt.QString(c), Qt.QVariant(c))
            self.blob2IOLayout.addWidget(blobNameColumnComboBox, i / 4 + 2, i % 4, 1, 1)			

        self.showMapColumnGrid(columnList, 'left')

        self.runButton1.setEnabled(True)


    def genFetchBlobSQL(self):
        BlobSQLText = QtGui.QTextEdit()
        targetTableName = str(self.targetDBText.text())
        targetTableColumn = []
        for w in self.mapColumnWidget.findChildren(Qt.QWidget, Qt.QRegExp('.*right.*')):
            targetTableColumn.append(w.currentText())

        sourceTableColumn = []
        for w in self.mapColumnWidget.findChildren(Qt.QWidget, Qt.QRegExp('.*left.*')):
            sourceTableColumn.append(w.currentText())

    def on_runButton_clicked(self):
        objName = self.sender().objectName()
        processes = str(self.processesEditor.text())
        processes = 0 if not processes else int(processes)        
        blobNameColumn = []
        if objName == 'run1':
            spliter = str(self.blobNameSplitText.text())
            for comboBox in self.blob2IOWidget.findChildren(Qt.QComboBox, Qt.QRegExp('blobNameColumnComboBox.*')):
                columnName = str(comboBox.currentText())
                if columnName:
                    blobNameColumn.append(columnName)
            filePath = str(self.ioPathEdit.text())
            self.control.runBlob2IO(spliter, blobNameColumn, filePath, processes)
        else:            
            mapColumnList = []
            for comboBox in self.blob2DBWidget.findChildren(Qt.QComboBox, Qt.QRegExp('mapColumnComboBox.*')):
                comboBoxName = str(comboBox.objectName())
                comboxNamePre, comboBoxDirec, comboBoxIndex = comboBoxName.split('-')
                comboBoxDirec = 0 if comboBoxDirec == 'left' else 1
                comboBoxIndex = int(comboBoxIndex)
                columnName = str(comboBox.currentText()) \
                    if comboBoxDirec == 0 else str(comboBox.currentText()).split(' ')[0]
                if len(mapColumnList) >= comboBoxIndex + 1:
                    mapColumnList[comboBoxIndex][comboBoxDirec] = columnName
                else:
                    mapColumnList.append([columnName, ''] if comboBoxDirec == 0 else ['', columnName])
             
            newMapColumn = []    
            if [i[0].upper() for i in mapColumnList].count('SQL2.IMAGE') == 0:
                self.mapColumnTipLabel.setText(u"* 请指定图片列的映射关系")
                return
            
            sourceColumn = [i[0] for i in mapColumnList]
            for l, r in mapColumnList:
                if not l or not r:
                    continue
                if mapColumnList.count([l, r]) > 1:
                    self.mapColumnTipLabel.setText(u"* 存在相同的列映射关系")
                    return
                if sourceColumn.count(l) > 1:
                    self.mapColumnTipLabel.setText(u"* 源表列中存在相同的列，请在SQL中使用不同的别名，以便区分")
                    print(mapColumnList, sourceColumn)
                    return

                
                newMapColumn.append([l, r])
            self.mapColumnTipLabel.setText(u"")
            self.control.runBlob2DB(newMapColumn, processes)            





if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = TaskEditor()
    ex.show()
    #ex.alarmClock([13])
    sys.exit(app.exec_())	

