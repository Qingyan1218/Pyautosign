import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
import ui_autosign
from autocadsign import autocadsign
import os.path


NAMETABLE={}
file=open('.\\name.cfg','r')
for line in file.readlines():
    line=line.rstrip().split(' ')
    if line[0]:
        NAMETABLE[line[0]]=line[1]
file.close()


# pyuic5 -o ui_autosign.py autosign.ui
# pyinstaller -F main.py --noconsole
class Autosign(QDialog,ui_autosign.Ui_Autosign):

    def __init__(self,  parent=None):
        super(Autosign, self).__init__(parent)
        self.setupUi(self)
        self.signButton.clicked.connect(self.setfile)

    def setfile(self):
        xd=self.XlineEdit.text().split(',')
        yd=self.YlineEdit.text().split(',')
        filedirection=self.AddresslineEdit.text()

        design=NAMETABLE[self.comboBox.currentText()]
        check=NAMETABLE[self.comboBox_2.currentText()]
        verify1=NAMETABLE[self.comboBox_3.currentText()]
        verify2=NAMETABLE[self.comboBox_4.currentText()]
        approve=NAMETABLE[self.comboBox_5.currentText()]
        middlenamelist = [design, check, verify1, verify2, approve]

        checklist=[self.checkBox1,self.checkBox2,self.checkBox3,self.checkBox4,self.checkBox5]

        datedesign=self.datelineEdit_1.text()
        datecheck = self.datelineEdit_2.text()
        dateverify1 = self.datelineEdit_3.text()
        dateverify2 = self.datelineEdit_4.text()
        dateapprove = self.datelineEdit_5.text()
        middledatelist=[datedesign,datecheck,dateverify1,dateverify2,dateapprove]

        atype_date=self.AtypelineEdit_2.text()
        atype_check = self.checkBox2_2.isChecked()
        atype_height=self.AtypelineEdit_3.text().split(',')
        Height=[int(atype_height[0]),int(atype_height[1])]
        # data用于记录签名位置
        namelist=[]
        datelist=[]
        data=[]
        a=0
        flag=True
        for check in checklist:
            if check.isChecked():
                data.append(a+1)
                if middlenamelist[a]=='':
                    QMessageBox.about(self,'Wrong','<p>lack name')
                    flag=False
                    break
                else:
                    namelist.append(middlenamelist[a])
                    datelist.append(middledatelist[a])
            a+=1
        if datelist[0]==None:
            datelist=None

        if flag==True:
            linedata=[[xd,yd],[i for i in data],[i for i in namelist]]
            try:
                autocadsign(atype_check,filedirection,linedata,datelist,atype_date,Height)
            except:
                QMessageBox.about(self, 'error', '<p>No sign file')
            QMessageBox.about(self,'notice','<p>Successfully')

if __name__=='__main__':
    app = QApplication(sys.argv)
    form = Autosign()
    form.show()
    app.exec_()
