from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from persiantools.jdatetime import JalaliDate
from PyQt5.QtWidgets import QTableWidget
from PyQt5.uic.properties import QtWidgets

import sys
import sqlite3


ui, _ = loadUiType('ATP_Club_manager.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.payment_for_type_zero = '370,000'
        self.payment_for_type_one = '70,000'
        self.handel_ui_changes()
        self.handel_buttons()
        self.create_table()

    def handel_ui_changes(self):
        self.themes()
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.set_date()
        self.show_users_in_table()
        QTableWidget.setSortingEnabled(self.tableWidget, True)
        self.lineEdit_22.setEnabled(False)
        self.lineEdit_23.setEnabled(False)
        self.lineEdit_24.setEnabled(False)
        self.lineEdit_25.setEnabled(False)
        self.lineEdit_26.setEnabled(False)
        self.lineEdit_16.setEnabled(False)
        self.lineEdit_13.setEnabled(False)
        self.lineEdit_17.setEnabled(False)
        self.lineEdit_12.setEnabled(False)
        self.lineEdit_15.setEnabled(False)
        self.lineEdit_20.setEnabled(False)
        self.check_payment_part()
        self.change_tab_order_register_part()
        self.change_tab_order_edit_part()
        self.change_tab_order_deleting_part()
        self.make_payment_part_stable()

    def handel_buttons(self):
        self.pushButton.clicked.connect(self.show_manager_part)
        self.pushButton_2.clicked.connect(self.show_users_part)
        self.pushButton_3.clicked.connect(self.show_calender_part)
        self.pushButton_10.clicked.connect(self.show_setting_part)
        self.pushButton_4.clicked.connect(self.show_payment_part)
        self.pushButton_9.clicked.connect(self.user_register)
        self.pushButton_5.clicked.connect(self.search_user)
        self.pushButton_6.clicked.connect(self.user_edit)
        self.pushButton_8.clicked.connect(self.search_user_delete)
        self.pushButton_7.clicked.connect(self.delete_users)
        self.pushButton_30.clicked.connect(self.serach_for_payment_part)
        self.pushButton_34.clicked.connect(self.show_data_in_table_payment_part)
        # self.pushButton_12.clicked.connect(self.change_payment_part)
        self.pushButton_11.clicked.connect(self.unlock_first_groupBox)
        self.pushButton_12.clicked.connect(self.change_user_name)
        self.pushButton_13.clicked.connect(self.change_password)
        self.pushButton_28.clicked.connect(self.sign_up)

    def themes(self):
        style = open('themes/qdark.css')
        style = style.read()
        self.setStyleSheet(style)

    ############################################################################
    ###############################Display part#################################

    def show_manager_part(self):
        self.tabWidget.setCurrentIndex(1)

    def show_users_part(self):
        self.tabWidget.setCurrentIndex(2)

    def show_calender_part(self):
        self.tabWidget.setCurrentIndex(3)

    def show_payment_part(self):
        self.tabWidget.setCurrentIndex(4)

    def show_setting_part(self):
        self.tabWidget.setCurrentIndex(5)

    def set_date(self):
        current_date = JalaliDate.today()

        self.lineEdit_18.setText(str(current_date))
        self.lineEdit_27.setText(str(current_date))

    def show_users_in_table(self):
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        self.cur.execute(
            'SELECT user_name , user_last_name , user_id , user_job , user_phone , date_register  , type FROM users ORDER BY user_last_name ASC')
        data = self.cur.fetchall()

        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if item == '1':
                    item = 'عادی'
                elif item == '0':
                    item = "خصوصی"

                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    def show_data_in_table_payment_part(self):
        user_name = self.lineEdit_22.text()
        user_last_name = self.lineEdit_23.text()
        user_id = self.lineEdit_24.text()
        user_payment = self.lineEdit_26.text()

        if user_name == "":
            QMessageBox.warning(self, "خطا", "لطفا شماره ملی کاربر مورد نظر را وارد کنید")

        elif user_last_name == "":
            QMessageBox.warning(self, "خطا", "لطفا شماره ملی کاربر مورد نظر را وارد کنید")

        elif user_id == "":
            QMessageBox.warning(self, "خطا", "لطفا شماره ملی کاربر مورد نظر را وارد کنید")

        elif user_payment == "":
            QMessageBox.warning(self, "خطا", "لطفا شماره ملی کاربر مورد نظر را وارد کنید")

        else:

            self.db = sqlite3.connect('data.db')
            self.cur = self.db.cursor()

            self.cur.execute('SELECT exp_date FROM users WHERE user_id = ?', (user_id,))
            data0 = self.cur.fetchone()

            self.db.close()

            e_date = data0[0]
            e_date_split = e_date.split('-')

            if int(e_date_split[1]) == 12:
                e_date_split[1] = '01'
                e_date_year = int(e_date_split[0]) + 1
                exp_date = str(e_date_year) + '-' + e_date_split[1] + '-' + e_date_split[2]

            elif int(e_date_split[1]) == 6  and int(e_date_split[2]) == 31:
                e_date_split[1] = '0' + str(int(e_date_split[1]) + 2)
                exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + '01'

            elif int(e_date_split[1]) == 1 or int(e_date_split[1]) == 2 or int(e_date_split[1]) == 3 or int(
                    e_date_split[1]) == 4 or int(e_date_split[1]) == 5 or int(e_date_split[1]) == 6 or int(
                e_date_split[1]) == 7 or int(e_date_split[1]) == 8:
                e_date_split[1] = '0' + str(int(e_date_split[1]) + 1)
                exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + e_date_split[2]

            else:
                e_date_split[1] = str(int(e_date_split[1]) + 1)
                exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + e_date_split[2]

            self.db = sqlite3.connect('data.db')
            self.cur = self.db.cursor()

            self.cur.execute('SELECT payment_part from users WHERE user_id = ?',(user_id,))
            data_payment = self.cur.fetchall()

            self.db.close()

            if data_payment[0] == 0:
                self.db = sqlite3.connect('data.db')
                self.cur = self.db.cursor()
                self.cur.execute('UPDATE users SET payment_part = ?  , exp_date = ? WHERE user_id = ?',
                                  (1, exp_date, user_id,))

                self.db.commit()
                self.db.close()

                self.db = sqlite3.connect('data.db')
                self.cur = self.db.cursor()

                self.cur.execute(
                    'SELECT user_name , user_last_name , user_id , date_register  , payment_part  , exp_date FROM users ORDER BY date_register ASC')
                data = self.cur.fetchall()

                self.db.close()

                self.tableWidget_3.setRowCount(0)

                today_date = self.lineEdit_27.text()

                for full_element in data:
                    if full_element[4] == 0 and int(full_element[5].split('-')[0] + full_element[5].split('-')[1] + full_element[5].split('-')[2]) <= int(today_date.split('-')[0] + today_date.split('-')[1] + today_date.split('-')[2]):
                        row_position = self.tableWidget_3.rowCount()
                        self.tableWidget_3.insertRow(row_position)
                        self.tableWidget_3.setItem(row_position, 0, QTableWidgetItem(str(full_element[0])))
                        self.tableWidget_3.setItem(row_position, 1, QTableWidgetItem(str(full_element[1])))
                        self.tableWidget_3.setItem(row_position, 2, QTableWidgetItem(str(full_element[2])))
                        self.tableWidget_3.setItem(row_position, 3, QTableWidgetItem(str(full_element[3])))

                    else:
                        continue

                self.db = sqlite3.connect('data.db')
                self.cur = self.db.cursor()

                self.cur.execute(
                    'SELECT user_name , user_last_name , user_id , date_register , type  , payment_part , exp_date FROM users ORDER BY user_last_name ASC')
                data2 = self.cur.fetchall()

                self.db.close()

                self.tableWidget_2.setRowCount(0)

                for full_element in data2:
                    if full_element[5] == 1:
                        row_position = self.tableWidget_2.rowCount()
                        self.tableWidget_2.insertRow(row_position)
                        self.tableWidget_2.setItem(row_position, 0, QTableWidgetItem(str(full_element[0])))
                        self.tableWidget_2.setItem(row_position, 1, QTableWidgetItem(str(full_element[1])))
                        self.tableWidget_2.setItem(row_position, 2, QTableWidgetItem(str(full_element[2])))

                        if full_element[4] == '0':
                            self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(self.payment_for_type_zero)))

                        elif full_element[4] == '1':
                            self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(self.payment_for_type_one)))

                        self.tableWidget_2.setItem(row_position , 4, QTableWidgetItem(str(full_element[6])))

                self.make_payment_part_stable()
            else:
                QMessageBox.warning(self,'خطا' , 'اشتراک کاربر مورد نظر تمام نشده است')

    def sign_up(self):
        flag = True
        user_name = self.lineEdit_47.text()
        password = self.lineEdit_48.text()

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
                self.lineEdit_47.setText('')
                self.lineEdit_48.setText('')

            else:
                QMessageBox.critical(self, 'خطا', "نام کاربری وارد شده تکراری است لطفا دوباره سعی کنید!")
                self.lineEdit_47.setText('')
                self.lineEdit_48.setText('')


    def make_payment_part_stable(self):
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        self.cur.execute(
            'SELECT user_name , user_last_name , user_id , date_register , type  , payment_part , exp_date FROM users ORDER BY exp_date ASC')
        data2 = self.cur.fetchall()

        self.db.close()

        self.tableWidget_2.setRowCount(0)

        for full_element in data2:
            if full_element[5] == 1:
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)
                self.tableWidget_2.setItem(row_position, 0, QTableWidgetItem(str(full_element[0])))
                self.tableWidget_2.setItem(row_position, 1, QTableWidgetItem(str(full_element[1])))
                self.tableWidget_2.setItem(row_position, 2, QTableWidgetItem(str(full_element[2])))

                if full_element[4] == '0':
                    self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(self.payment_for_type_zero)))

                elif full_element[4] == '1':
                    self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(self.payment_for_type_one)))

                self.tableWidget_2.setItem(row_position, 4, QTableWidgetItem(str(full_element[6])))
            else:
                continue

    def check_payment_part(self):
        today_date = self.lineEdit_27.text()

        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        self.cur.execute(
            'SELECT user_name , user_last_name , user_id , date_register , payment_part , exp_date FROM users ORDER BY date_register ASC')

        data = self.cur.fetchall()
        self.db.close()


        for full_element in data:
            if full_element[5] == today_date or int(full_element[5].split('-')[0] + full_element[5].split('-')[1] + full_element[5].split('-')[2]) < int(today_date.split('-')[0] + today_date.split('-')[1] + today_date.split('-')[2]):
                self.db = sqlite3.connect('data.db')
                self.cur = self.db.cursor()

                self.cur.execute('UPDATE users SET payment_part = ? WHERE exp_date = ?', (0, full_element[5],))

                self.db.commit()
                self.db.close()

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
                self.tableWidget_3.setItem(row_position, 0, QTableWidgetItem(str(full_element[0])))
                self.tableWidget_3.setItem(row_position, 1, QTableWidgetItem(str(full_element[1])))
                self.tableWidget_3.setItem(row_position, 2, QTableWidgetItem(str(full_element[2])))
                self.tableWidget_3.setItem(row_position, 3, QTableWidgetItem(str(full_element[3])))

            else:
                continue

    def change_tab_order_register_part(self):
        self.setTabOrder(self.lineEdit_5, self.lineEdit_18)
        self.setTabOrder(self.lineEdit_18, self.comboBox)
        self.setTabOrder(self.comboBox, self.pushButton_9)

    def change_tab_order_edit_part(self):
        self.setTabOrder(self.lineEdit_11, self.pushButton_5)
        self.setTabOrder(self.pushButton_5, self.lineEdit_8)
        self.setTabOrder(self.lineEdit_8, self.lineEdit_9)
        self.setTabOrder(self.lineEdit_9, self.lineEdit_10)
        self.setTabOrder(self.lineEdit_6, self.lineEdit_19)
        self.setTabOrder(self.lineEdit_19, self.comboBox_2)
        self.setTabOrder(self.comboBox_2, self.pushButton_6)

    def change_tab_order_deleting_part(self):
        self.setTabOrder(self.lineEdit_14, self.pushButton_8)
        self.setTabOrder(self.pushButton_8, self.pushButton_7)

    ###################################################################
    ###############################Database############################

    def create_table(self):
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS users(idusers integer primary key AUTOINCREMENT , user_name text, user_last_name text, user_id text, user_job text, user_phone text, date_register date, type text , payment_part integer , exp_date date)')

        self.db.commit()
        self.db.close()

    ############################################################################
    #############################USER##################################

    def user_register(self):
        user_name = self.lineEdit.text()
        user_last_name = self.lineEdit_2.text()
        user_id = self.lineEdit_3.text()
        user_job = self.lineEdit_4.text()
        user_phone = self.lineEdit_5.text()
        date_register = self.lineEdit_18.text()
        user_type = self.comboBox.currentIndex()

        e_date = self.lineEdit_18.text()
        e_date_split = e_date.split('-')

        if int(e_date_split[1]) == 12:
            e_date_split[1] = '01'
            e_date_year = int(e_date_split[0]) + 1
            exp_date = str(e_date_year) + '-' + e_date_split[1] + '-' + e_date_split[2]

        elif int(e_date_split[1]) == 6 and int(e_date_split[2]) == 31:
            e_date_split[1] = '0' + str(int(e_date_split[1]) + 2)
            exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + '01'

        elif int(e_date_split[1]) == 1 or int(e_date_split[1]) == 2 or int(e_date_split[1]) == 3 or int(
                e_date_split[1]) == 4 or int(e_date_split[1]) == 5 or int(e_date_split[1]) == 6 or int(
                e_date_split[1]) == 7 or int(e_date_split[1]) == 8:
            e_date_split[1] = '0' + str(int(e_date_split[1]) + 1)
            exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + e_date_split[2]

        else:
            e_date_split[1] = str(int(e_date_split[1]) + 1)
            exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + e_date_split[2]

        if user_name == "":
            QMessageBox.critical(self, 'خطا', "لطفا اطلاعات را به صورت کامل وارد کنید")

        elif user_last_name == "":
            QMessageBox.critical(self, 'خطا', "لطفا اطلاعات را به صورت کامل وارد کنید")

        elif user_id == "":
            QMessageBox.critical(self, 'خطا', "لطفا اطلاعات را به صورت کامل وارد کنید")

        elif date_register == "":
            QMessageBox.critical(self, 'خطا', "لطفا اطلاعات را به صورت کامل وارد کنید")

        else:

            self.db = sqlite3.connect('data.db')
            self.cur = self.db.cursor()

            sql = 'INSERT INTO users(user_name , user_last_name , user_id , user_job , user_phone , date_register , type , payment_part , exp_date) VALUES(? , ? , ? , ? , ? , ? , ? , ? , ?)'
            self.cur.execute(sql, (
            user_name, user_last_name, user_id, user_job, user_phone, date_register, user_type, 1, exp_date))

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('New user added')

            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")

            row_position = self.tableWidget_2.rowCount()

            self.tableWidget_2.insertRow(row_position)
            self.tableWidget_2.setItem(row_position, 0, QTableWidgetItem(str(user_name)))
            self.tableWidget_2.setItem(row_position, 1, QTableWidgetItem(str(user_last_name)))
            self.tableWidget_2.setItem(row_position, 2, QTableWidgetItem(str(user_id)))

            if user_type == 0:
                self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(self.payment_for_type_zero)))
            elif user_type == 1:
                self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(self.payment_for_type_one)))


            self.set_date()

            self.tableWidget.setRowCount(0)
            self.show_users_in_table()

    def search_user(self):
        user_id = self.lineEdit_11.text()

        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        sql = 'SELECT * FROM users WHERE user_id = ?'

        self.cur.execute(sql, (user_id,))
        data = self.cur.fetchone()

        if (data == None):
            QMessageBox.critical(self, "خطا", "کد ملی وارد شده نامعتبر است!")
            self.db.close()

        else:
            self.lineEdit_8.setText(data[1])
            self.lineEdit_9.setText(data[2])
            self.lineEdit_10.setText(data[3])
            # self.lineEdit_7.setText(data[4])
            self.lineEdit_6.setText(data[5])
            self.lineEdit_19.setText(data[6])
            self.comboBox_2.setCurrentIndex(int(data[7]))
            self.lineEdit_34.setText(data[9])

            self.db.close()

            self.statusBar().showMessage('Information matched')

    def search_user_delete(self):
        user_id = self.lineEdit_14.text()

        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        sql = 'SELECT * FROM users WHERE user_id = ?'

        self.cur.execute(sql, (user_id,))
        data = self.cur.fetchone()

        if (data == None):
            QMessageBox.critical(self, 'خطا', "کد ملی وارد شده نامعتبر است")
            self.db.close()

        else:
            self.lineEdit_16.setText(data[1])
            self.lineEdit_13.setText(data[2])
            self.lineEdit_17.setText(data[3])
            self.lineEdit_12.setText(data[4])
            self.lineEdit_15.setText(data[5])
            self.lineEdit_20.setText(data[6])
            self.comboBox_3.setCurrentIndex(int(data[7]))

            self.db.close()
            self.statusBar().showMessage('Information matched')

    def user_edit(self):
        user_ex_id = self.lineEdit_11.text()
        user_name = self.lineEdit_8.text()
        user_last_name = self.lineEdit_9.text()
        user_id = self.lineEdit_10.text()
        # user_job = self.lineEdit_7.text()
        user_phone = self.lineEdit_6.text()
        date_register = self.lineEdit_19.text()
        user_type = self.comboBox_2.currentIndex()
        exp_date = self.lineEdit_34.text()

        # e_date = date_register
        # e_date_split = e_date.split('-')
        # print(e_date)
        #
        # if int(e_date_split[1]) == 12:
        #     e_date_split[1] = '01'
        #     e_date_year = int(e_date_split[0]) + 1
        #     exp_date = str(e_date_year) + '-' + e_date_split[1] + '-' + e_date_split[2]
        #
        # elif int(e_date_split[1]) == 6 and int(e_date_split[2]) == 31:
        #     e_date_split[1] = '0' + str(int(e_date_split[1]) + 2)
        #     exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + '01'
        #
        # elif int(e_date_split[1]) == 1 or int(e_date_split[1]) == 2 or int(e_date_split[1]) == 3 or int(
        #         e_date_split[1]) == 4 or int(e_date_split[1]) == 5 or int(e_date_split[1]) == 6 or int(
        #     e_date_split[1]) == 7 or int(e_date_split[1]) == 8:
        #     e_date_split[1] = '0' + str(int(e_date_split[1]) + 1)
        #     exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + e_date_split[2]
        #
        # else:
        #     e_date_split[1] = str(int(e_date_split[1]) + 1)
        #     exp_date = e_date_split[0] + '-' + e_date_split[1] + '-' + e_date_split[2]

        if user_name == '':
            QMessageBox.critical(self, 'خطا', "لطفا کد ملی کاربر مورد نظر راوارد کنید ")

        elif user_last_name == '':
            QMessageBox.critical(self, 'خطا', "لطفا کد ملی کاربر مورد نظر راوارد کنید ")

        elif user_id == '':
            QMessageBox.critical(self, 'خطا', "لطفا کد ملی کاربر مورد نظر راوارد کنید ")

        # elif user_job == '':
        #     QMessageBox.critical(self, 'خطا', "لطفا کد ملی کاربر مورد نظر راوارد کنید ")

        elif user_phone == '':
            QMessageBox.critical(self, 'خطا', "لطفا کد ملی کاربر مورد نظر راوارد کنید ")

        elif date_register == '':
            QMessageBox.critical(self, 'خطا', "لطفا کد ملی کاربر مورد نظر راوارد کنید ")

        else:
            self.db = sqlite3.connect('data.db')
            self.cur = self.db.cursor()

            question = QMessageBox.question(self, "Message", "تغیرات مورد نظر اعمال شود؟",
                                            QMessageBox.Yes | QMessageBox.No)

            if question == QMessageBox.Yes:
                if date_register == self.lineEdit_27.text():
                    sql = 'UPDATE users SET user_name=? , user_last_name=? , user_id=? , user_phone=? , date_register=? , type=? , payment_part=?  , exp_date=? WHERE user_id=?'
                    self.cur.execute(sql, (
                        user_name, user_last_name, user_id, user_phone, date_register, user_type, 1 ,exp_date,
                        user_ex_id,))

                    self.db.commit()
                    self.db.close()
                else:

                    sql = 'UPDATE users SET user_name=? , user_last_name=? , user_id=? , user_phone=? , date_register=? , type=?  , exp_date=? WHERE user_id=?'
                    self.cur.execute(sql, (
                        user_name, user_last_name, user_id, user_phone, date_register, user_type, exp_date ,user_ex_id,))

                    self.db.commit()
                    self.db.close()

                self.statusBar().showMessage("User edited")
                self.make_payment_part_stable()
                self.lineEdit_11.setText("")
                self.lineEdit_8.setText("")
                self.lineEdit_9.setText("")
                self.lineEdit_10.setText("")
                self.lineEdit_34.setText("")
                self.lineEdit_6.setText("")
                self.lineEdit_19.setText("")

                self.tableWidget.setRowCount(0)
                self.show_users_in_table()
                self.tableWidget_3.setRowCount(0)
                self.check_payment_part()


    def delete_users(self):
        user_ex_id = self.lineEdit_14.text()
        user_id = self.lineEdit_17.text()

        if user_ex_id == '' or user_id == '':
            QMessageBox.critical(self, "خطا", "لطفا کد ملی کاربر مورد نظر را وارد کنید")

        else:
            self.db = sqlite3.connect('data.db')
            self.cur = self.db.cursor()

            question = QMessageBox.question(self, "Message", "اطلاعات مربوط به کاربر حذف شود؟",
                                            QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:
                sql = 'DELETE FROM users WHERE user_id = ?'
                self.cur.execute(sql, (user_ex_id,))

                self.db.commit()
                self.db.close()
                self.statusBar().showMessage("User deleted")

                self.lineEdit_14.setText("")
                self.lineEdit_16.setText("")
                self.lineEdit_13.setText("")
                self.lineEdit_17.setText("")
                self.lineEdit_12.setText("")
                self.lineEdit_15.setText("")
                self.lineEdit_20.setText("")
                self.tableWidget.setRowCount(0)
                self.show_users_in_table()
                self.tableWidget_3.setRowCount(0)
                self.check_payment_part()

    ##########################################################################
    ############################Payment part##################################

    def serach_for_payment_part(self):
        user_id = self.lineEdit_21.text()
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

        self.cur.execute(
            'SELECT user_name , user_last_name , user_id , date_register , type FROM users WHERE user_id = ?',
            (user_id,))
        data = self.cur.fetchone()
        self.db.close()
        if data == None:
            QMessageBox.critical(self, 'خطا', "کد ملی وارد شده نامعتبر است")
        else:
            self.lineEdit_22.setText(data[0])
            self.lineEdit_23.setText(data[1])
            self.lineEdit_24.setText(data[2])
            self.lineEdit_25.setText(data[3])

            if data[4] == '0':
                self.lineEdit_26.setText(self.payment_for_type_zero)

            elif data[4] == '1':
                self.lineEdit_26.setText(self.payment_for_type_one)

        self.lineEdit_21.setText("")
#######################################################################
#######################################################################

    def change_payment_part(self):
        payment_for_type_zoro = self.lineEdit_30.text()
        payment_for_type_one = self.lineEdit_31.text()

        self.lineEdit_30.setText(payment_for_type_zoro)
        self.lineEdit_31.setText(payment_for_type_one)

    def unlock_first_groupBox(self):
        user_name = self.lineEdit_28.text()
        password = self.lineEdit_29.text()

        self.db = sqlite3.connect('data_managers.db')
        self.cur = self.db.cursor()

        self.cur.execute('SELECT * FROM managers')
        data = self.cur.fetchall()

        self.db.close()

        flag = False
        for full_element in data:
            if full_element[1] == user_name and full_element[2] == password:
                self.groupBox.setEnabled(True)
                self.groupBox_3.setEnabled(True)
                self.lineEdit_30.setText(full_element[1])
                self.lineEdit_31.setText(full_element[2])
                flag = True
                break
            else:
                flag = False
                continue

        if flag == False:
            QMessageBox.warning(self,'خطا','نام کاربری یا رمز عبور اشتباه وارد شده است!')
        else:
            self.statusBar().showMessage('Information matched')

    def change_user_name(self):
        user_name = self.lineEdit_28.text()
        new_user_name = self.lineEdit_30.text()

        self.db = sqlite3.connect('data_managers.db')
        self.cur = self.db.cursor()

        self.cur.execute('UPDATE managers SET manager_user_name = ? WHERE manager_user_name = ?' , (new_user_name , user_name,))

        self.db.commit()
        self.db.close()

        self.statusBar().showMessage('Well Done')

    def change_password(self):
        user_name = self.lineEdit_30.text()
        new_password = self.lineEdit_31.text()

        self.db = sqlite3.connect('data_managers.db')
        self.cur = self.db.cursor()

        self.cur.execute('UPDATE managers SET password = ? WHERE manager_user_name = ?' , (new_password , user_name ,))

        self.db.commit()
        self.db.close()




def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
