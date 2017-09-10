# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
import time
import sys
from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore
from enum import Enum

class TypeEnum(Enum):
    success = 1
    error = 2

class GoogleSearch:

    def __init__(self):
        chromedriver = "chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.get('')

    def fillForm(self,autoFillFormApplication,javascript):
        isValid = True
        autoFillFormApplication.setLogEditText(u"填寫表單....")
        try:
            # step1 
            self.driver.execute_script(javascript)
            submitButton = self.driver.find_element_by_xpath("//div[@class='btnGroup']/button[@type='submit']")
            submitButton.click()

        except NoSuchElementException:
            autoFillFormApplication.setLogEditText(NoSuchElementException.message)
            return

        try:
            WebDriverWait(self.driver, 1).until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            alert.accept()
            autoFillFormApplication.setLogEditText(u"資料輸入有誤,請再次確認")
            print("[*]Email error")
        except TimeoutException:
            autoFillFormApplication.setLogEditText(u"資料輸入正確")
            autoFillFormApplication.setLogEditText(u"No alert ")
            return
      
    def cancelOrder(self,autoFillFormApplication):
        text = []
        try:
            trList = self.driver.find_elements_by_xpath("//*[@id='cont']/table/tbody/tr")
            for tr in trList:
                text.append(tr.text)
        except NoSuchElementException:
            autoFillFormApplication.setLogEditText(NoSuchElementException.message)
            return

        try:
            cancelButton = self.driver.find_element_by_xpath("//div[@class='btnGroup']/button[2]")
            cancelButton.click()
        except NoSuchElementException:
            autoFillFormApplication.setLogEditText(u"資料可能有填寫錯誤")
            autoFillFormApplication.showDialog(TypeEnum.error,u"資料可能有填寫錯誤")
            return
        except Exeption as exception:
            autoFillFormApplication.setLogEditText(exception)
            autoFillFormApplication.setLogEditText(u"程式發生異常")
            return

        try:
            WebDriverWait(self.driver, 1).until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            alert.accept()
        except TimeoutException:
            autoFillFormApplication.setLogEditText(u"No alert ")
            return
        except Exception:
            autoFillFormApplication.setLogEditText(Exception.message)
            return
        autoFillFormApplication.showDialog(TypeEnum.success,text)
        self.driver.quit()

class AutoFillFormApplication(QtGui.QWidget):

    def __init__(self, *args):
        super(AutoFillFormApplication, self).__init__(*args)
        self.initUI()

    def initUI(self):
        # 元件設定 
        javascriptCode = QtGui.QLabel(u'程式碼')
        log = QtGui.QLabel(u'紀錄')
        submitButton = QtGui.QPushButton(u"提交")
        closeButton = QtGui.QPushButton(u"關閉")
        self.javascriptCodeEdit = QtGui.QLineEdit()
        self.logEdit = QtGui.QTextEdit()

        # 樣式設定
        submitButton.setFixedSize(75,25)
        closeButton.setFixedSize(75,25)

        # 事件設定
        self.connect(submitButton,Qt.SIGNAL("clicked()"),self.openWebPageAndFillForm)
        self.connect(closeButton,Qt.SIGNAL("clicked()"),self.closeApplication)
        
        # 排版設定
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(javascriptCode, 1, 0) # (widget,row,column)
        grid.addWidget(self.javascriptCodeEdit, 1, 1) # (widget,row,column)

        grid.addWidget(log, 2, 0)
        grid.addWidget(self.logEdit, 2, 1, 5, 1) # (widget,row,column,row span,column span)
        
        grid.addWidget(submitButton,8,1)
        grid.addWidget(closeButton,8,2,1,1)
       
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle(u"demo")     
        self.show() # 每個元件一開始都是隱藏的,所以要顯示

    def openWebPageAndFillForm(self):
        self.setLogEditText(u"開起網頁....")
        googleSearch = GoogleSearch()
        javascript= self.javascriptCodeEdit.text().toUtf8()
        googleSearch.fillForm(self,str(javascript))
        time.sleep(1)
        googleSearch.cancelOrder(self)
        return
        
        
    def closeApplication(self):
        QtGui.QApplication.quit()
        sys.exit()

    def setLogEditText(self,text):
        self.logEdit.append("[*] %s \n" %(text))

    def showDialog(self,typeEnum,text):
        icon = QtGui.QMessageBox.Information
        dialogTextList =text
        title =u"結果資訊"
        text = ""
        if(typeEnum is TypeEnum.success):
            icon = QtGui.QMessageBox.Information
            text = [str(x) for x in dialogTextList]
            text = '\n'.join(text)
        elif(typeEnum is TypeEnum.error):
            icon = QtGui.QMessageBox.Warning
            text = u"資料填寫可能有誤,請再次確認"

        msg = QtGui.QMessageBox(self)
        msg.setIcon(icon)
        msg.setText(unicode(str(text)))
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msg.exec_() # 顯示messagebox

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    app = QtGui.QApplication(sys.argv) # 啟動應用程式
    autoFillFormApplication = AutoFillFormApplication()
    sys.exit(app.exec_())  

