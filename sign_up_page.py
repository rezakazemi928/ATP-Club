from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import system as sh

import sys
import sqlite3

ui, _ = loadUiType('sign_up_managers.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_ui_changes()
        self.handel_buttons()

    def handel_ui_changes(self):
        self.themes()

    def handel_buttons(self):
        self.pushButton.clicked.connect(self.sign_up)
        self.pushButton_2.clicked.connect(self.back_to_login_page)

    def back_to_login_page(self):
        self.close()
        sh("python login_page.py")

    def sign_up(self):
        flag = True
        user_name = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if user_name == '':
            QMessageBox.critical(self ,'خطا', "لطفا نام کاربری خود را وارد کنید.")

        elif password == '':
            QMessageBox.critical(self ,'خطا', "لطفا رمز عبور خود را وارد.")

        else:
            self.db = sqlite3.connect('data_managers.db')
            self.cur = self.db.cursor()

            self.cur.execute('SELECT * FROM managers WHERE manager_user_name = ?', (user_name,))

            data = self.cur.fetchall()

            self.db.close()

            for full_element in data:
                for element in full_element:
                    if user_name == element:
                        flag = False
                        break

                    else:
                        flag = True
                        continue


            if flag == True:

                self.db = sqlite3.connect('data_managers.db')
                self.cur = self.db.cursor()

                self.cur.execute('INSERT INTO managers(manager_user_name , password) VALUES(? , ?)' , (user_name , password,))

                self.db.commit()
                self.db.close()

                self.statusBar().showMessage('New managers added')
                QMessageBox.information(self , 'INFO' , "کاربر جدید برای بخش مدیران اضافه شد!")

                self.close()
                sh("python login_page.py")

            else:
                QMessageBox.critical(self, 'خطا', "نام کاربری وارد شده تکراری است لطفا دوباره سعی کنید!")
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')

    def themes(self):
        style = open('themes/qdark.css')
        style = style.read()
        self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()