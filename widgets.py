import wmi
import authorization

import threading

from internet_functions import ping, upload_speed, download_speed
from user_exceptions import NoFileName

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_widget_design.ui", self)
        self.connect_buttons()
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Показометр скорости интернета и параметров компьютера")

        self.total_hardware_list = []
        self.total_internet_list = []
        self.hardware_filename = ""
        self.internet_filename = ""
    
    def connect_buttons(self):
        self.display_hardware_btn.clicked.connect(self.display_hardware)
        self.write_hardware_btn.clicked.connect(self.write_hardware)
        self.choose_all_hardware_btn.clicked.connect(self.choose_all_hardware)
        self.display_internet_btn.clicked.connect(self.display_internet)
        self.write_internet_btn.clicked.connect(self.write_internet)
        self.choose_all_internet_btn.clicked.connect(self.choose_all_internet)
    
    def display_hardware(self):
        self.hardware_listwidget.addItem("Подождите...")

        self.set_hardware_list()
        self.hardware_listwidget.clear()
        self.hardware_listwidget.addItems(self.total_hardware_list)

    def write_hardware(self):
        self.hardware_error_label.setText("")
        self.hardware_error_label.setStyleSheet("color: red")
        self.hardware_filename = self.hardware_filename_lineedit.text()

        if not self.hardware_filename:
            self.hardware_error_label.setText("Введите имя файла!")
            return
        try:
            if not self.hardware_filename:
                raise NoFileName

            if len(self.hardware_filename.split(".")) == 1:
                self.hardware_filename += ".txt"
            elif len(self.hardware_filename.split(".")) == 1 and\
                    not self.hardware_filename.split(".")[1]:
                self.hardware_filename += "txt"
            
            with open(self.hardware_filename, 'w') as text_file:
                self.set_hardware_list()

                for parameter in self.total_hardware_list:
                    text_file.write(parameter + "\n")
                
                self.hardware_error_label.setStyleSheet("color: green")
                self.hardware_error_label.setText("Готово!")
        except NoFileName:
            self.hardware_error_label.setText("Вы забыли написать имя файла!")

    def choose_all_hardware(self):
        self.manufacturer_box.setChecked(True)
        self.pc_model_box.setChecked(True)
        self.os_name_box.setChecked(True)
        self.os_version_box.setChecked(True)
        self.cpu_name_box.setChecked(True)
        self.ram_box.setChecked(True)
        self.gpu_box.setChecked(True)

    def display_internet(self):
        self.set_internet_list()
        self.internet_listwidget.clear()
        self.internet_listwidget.addItems(self.total_internet_list)

    def write_internet(self):
        self.internet_error_label.setText("")
        self.internet_error_label.setStyleSheet("color: red")
        self.internet_filename = self.internet_filename_lineedit.text()
        
        try:
            if not self.internet_filename:
                raise NoFileName
            
            if len(self.internet_filename.split(".")) == 1:
                self.internet_filename += ".txt"
            elif len(self.internet_filename.split(".")) == 2 and\
                    not self.internet_filename.split(".")[1]:
                self.internet_filename += "txt"
            
            with open(self.internet_filename, "w") as text_file:
                self.set_internet_list()

                for parameter in self.total_internet_list:
                    text_file.write(parameter + "\n")
                
                self.internet_error_label.setStyleSheet("color: green")
                self.internet_error_label.setText("Готово!")
        except NoFileName:
            self.internet_error_label.setText("Вы забыли написать имя файла!")

    def choose_all_internet(self):
        self.ping_box.setChecked(True)
        self.upload_box.setChecked(True)
        self.download_box.setChecked(True)

    def set_hardware_list(self):

        self.total_hardware_list = []
        computer = wmi.WMI()

        computer_info = computer.Win32_ComputerSystem()[0]
        os_info = computer.Win32_OperatingSystem()[0]

        if self.manufacturer_box.checkState():
            self.total_hardware_list.append(f"Производитель: {computer_info.Manufacturer}")

        if self.pc_model_box.checkState():
            self.total_hardware_list.append(f"Модель: {computer_info.Model}")
        
        if self.os_name_box.checkState():
            os_name = os_info.Name.encode("utf-8").split(b"|")[0].decode()
            self.total_hardware_list.append(f"Имя ОС: {os_name}")
        
        if self.os_version_box.checkState():
            os_version = ' '.join([os_info.Version, os_info.BuildNumber])
            self.total_hardware_list.append(f"Версия ОС: {os_version}")
        
        if self.cpu_name_box.checkState():
            cpu_info = computer.Win32_Processor()[0].Name
            self.total_hardware_list.append(f"Название процессора: {cpu_info}")
        
        if self.ram_box.checkState():
            ram = round(float(os_info.TotalVisibleMemorySize) / 1024 / 1024, 2)
            self.total_hardware_list.append(f"Объем ОЗУ: {ram}")
        
        if self.gpu_box.checkState():
            gpu_info = computer.Win32_VideoController()

            if len(gpu_info) > 1:
                for i, card in enumerate(gpu_info, 1):
                    self.total_hardware_list.append(f"Видеокарта номер {i}: {card.Name}")
            else:
                self.total_hardware_list.append(gpu_info[0].Name)

    def set_internet_list(self):
        self.total_internet_list = []

        if self.ping_box.checkState():
            self.total_internet_list.append(f"Ping: {ping()}")
        
        if self.upload_box.checkState():
            self.total_internet_list.append(f"Скорость загрузки: {upload_speed()}")
        
        if self.download_box.checkState():
            self.total_internet_list.append(f"Скорость скачивания: {download_speed()}")

        self.internet_error_label.setText("")


class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("authorization_window_design.ui", self)
        self.connect_buttons()
    
    def connect_buttons(self):
        self.sign_in_btn.clicked.connect(self.try_to_sign_in)
        self.make_acc_btn.clicked.connect(self.make_a_profile)
    
    def parse_data(self):
        login = self.login_lineEdit.text()
        password = self.password_lineEdit.text()
        return (login, password)
    
    def try_to_sign_in(self):
        global authorized
        if authorization.find_in_db(*self.parse_data()):
            authorized = True
            self.close()
        else:
            self.error_lbl.setText("Неверный логин или пароль")        
    
    def make_a_profile(self):
        authorization.add_in_db(*self.parse_data())
        self.error_lbl.setText("")
