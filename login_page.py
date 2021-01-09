from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType


import sys
import sqlite3

from os import system as sh
from sign_up_page import MainApp as obj1

ui,_ = loadUiType('ATP_Club_login.ui')
# ui2,_ = loadUiType('sign_up_managers.ui')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_ui_changes()
        self.handel_buttons()

    def handel_ui_changes(self):
        self.themes()
        self.create_tabale_managers()

    def handel_buttons(self):
        self.pushButton.clicked.connect(self.log_in)
        # self.pushButton_2.clicked.connect(self.load_sign_up_page)


    def log_in(self):
        user_name = self.lineEdit.text()
        password = self.lineEdit_2.text()

        self.db = sqlite3.connect('data_managers.db')
        self.cur = self.db.cursor()

        self.cur.execute('SELECT * FROM managers WHERE manager_user_name = ?' , (user_name,))
        data = self.cur.fetchone()

        self.db.close()

        if data == None:
            QMessageBox.critical(self, 'خطا', 'نام کاربری یا رمز عبور وارد شده صحیح نیست')

        elif user_name == data[1] and password == data[2]:
            self.close()
            sh("python manager_page.py")

        else:
            QMessageBox.critical(self,'خطا', 'نام کاربری یا رمز عبور وارد شده صحیح نیست')

    def themes(self):
        style = open('themes/qdark.css')
        style = style.read()
        self.setStyleSheet(style)

    def create_tabale_managers(self):
        self.db = sqlite3.connect('data_managers.db')
        self.cur = self.db.cursor()

        self.cur.execute('CREATE TABLE IF NOT EXISTS managers(managerid integer primary key AUTOINCREMENT , manager_user_name text , password text)')

        self.db.commit()
        self.db.close()

    def load_sign_up_page(self):
        self.close()
        sh("python sign_up_page.py")
        obj1.sign_up()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()