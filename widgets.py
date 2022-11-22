import wmi
import authorization


from internet_functions import ping, upload_speed, download_speed
from user_exceptions import NoFileName

from speedtest import SpeedtestBestServerFailure
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QDialog, QLineEdit, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_widget_design.ui", self)
        self.connect_buttons()
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Показометр скорости интернета и параметров компьютера")
        self.internet_progressBar.setValue(0)
        self.hardware_progressBar.setValue(0)

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
    
    def display_hardware(self):  # Отобразить параметры ПК
        self.set_hardware_list()
        self.hardware_listwidget.clear()
        self.hardware_listwidget.addItems(self.total_hardware_list)

    def write_hardware(self):  # Записать параметры ПК в файл
        self.hardware_error_label.setText("")
        self.hardware_error_label.setStyleSheet("color: red")
        self.hardware_filename = self.hardware_filename_lineedit.text()

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

    def choose_all_hardware(self):  # Выбрать все галочки параметров компьютера
        self.manufacturer_box.setChecked(True)
        self.pc_model_box.setChecked(True)
        self.os_name_box.setChecked(True)
        self.os_version_box.setChecked(True)
        self.cpu_name_box.setChecked(True)
        self.ram_box.setChecked(True)
        self.gpu_box.setChecked(True)

    def display_internet(self):  # Отобразить параметры интернета
        self.internet_progressBar.setValue(0)
        self.set_internet_list()
        self.internet_listwidget.clear()
        self.internet_listwidget.addItems(self.total_internet_list)

    def write_internet(self):  # Записать параметры интернета в файл
        self.internet_error_label.setText("")
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
            self.internet_error_label.setStyleSheet("color: red")
            self.internet_error_label.setText("Вы забыли написать имя файла!")

    def choose_all_internet(self):  # Выбрать все галочки интернета
        self.ping_box.setChecked(True)
        self.upload_box.setChecked(True)
        self.download_box.setChecked(True)

    def set_hardware_list(self):  # Сформировать список с параметрами компьютера
        self.hardware_error_label.setText("Подождите...")
        self.hardware_progressBar.setValue(0)
        self.total_hardware_list = []
        computer = wmi.WMI()

        computer_info = computer.Win32_ComputerSystem()[0]
        os_info = computer.Win32_OperatingSystem()[0]

        if self.manufacturer_box.checkState():
            self.total_hardware_list.append(f"Производитель: {computer_info.Manufacturer}")
        self.hardware_progressBar.setValue(14)

        if self.pc_model_box.checkState():
            self.total_hardware_list.append(f"Модель: {computer_info.Model}")
        self.hardware_progressBar.setValue(29)
        
        if self.os_name_box.checkState():
            os_name = os_info.Name.encode("utf-8").split(b"|")[0].decode()
            self.total_hardware_list.append(f"Имя ОС: {os_name}")
        self.hardware_progressBar.setValue(44)
        
        if self.os_version_box.checkState():
            os_version = ' '.join([os_info.Version, os_info.BuildNumber])
            self.total_hardware_list.append(f"Версия ОС: {os_version}")
        self.hardware_progressBar.setValue(59)
        
        if self.cpu_name_box.checkState():
            cpu_info = computer.Win32_Processor()[0]
            self.total_hardware_list.append(f"Название процессора: {cpu_info.Name}")
            self.total_hardware_list.append(f"Количество ядер процессора: {cpu_info.NumberOfCores}")
            self.total_hardware_list.append(f"Количество потоков процессора: {cpu_info.ThreadCount}")
        self.hardware_progressBar.setValue(73)
        
        if self.ram_box.checkState():
            ram = round(float(os_info.TotalVisibleMemorySize) / 1024 / 1024, 2)
            self.total_hardware_list.append(f"Объем ОЗУ: {ram} ГБ")
        self.hardware_progressBar.setValue(88)
        
        if self.gpu_box.checkState():
            gpu_info = computer.Win32_VideoController()

            if len(gpu_info) > 1:
                for i, card in enumerate(gpu_info, 1):
                    self.total_hardware_list.append(f"Видеокарта номер {i}: {card.Name}")
            else:
                self.total_hardware_list.append(f"Видеокарта: {gpu_info[0].Name}")

        self.hardware_error_label.setText("")
        self.hardware_progressBar.setValue(100)

    def set_internet_list(self):  # Сформировать список с параметрами интернета
        self.internet_error_label.setText("Подождите...")

        try:
            self.total_internet_list = []

            if self.ping_box.checkState():
                addr = self.ping_lineEdit.text()
                if addr != "":
                    self.total_internet_list.append(f"Ping: {ping(addr)}")
                else:
                    self.total_internet_list.append(F"Ping: {ping()}")
                    self.ping_lineEdit.setText("yandex.ru")
            self.internet_progressBar.setValue(30)

            if self.upload_box.checkState():
                self.total_internet_list.append(f"Скорость загрузки: {upload_speed()}")
            self.internet_progressBar.setValue(65)

            if self.download_box.checkState():
                self.total_internet_list.append(f"Скорость скачивания: {download_speed()}")
            self.internet_error_label.setText("")

            self.internet_progressBar.setValue(100)
        except SpeedtestBestServerFailure:
            self.internet_error_label.setStyleSheet("color: red")
            self.internet_error_label.setText("Нет подключения к сети")

        self.internet_error_label.setText("")


class Login(QDialog):  # Диалоговое окно для авторизации
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowTitle("Авторизация")
        self.username_lineEdit = QLineEdit(self)
        self.password_lineEdit = QLineEdit(self)

        self.go_btn = QPushButton('Войти', self)
        self.reg_btn = QPushButton("Зарегистрироваться", self)
        self.go_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.registrate)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Логин:", self))
        layout.addWidget(self.username_lineEdit)
        layout.addWidget(QLabel("Пароль (заполняется после проверки логина):", self))
        layout.addWidget(self.password_lineEdit)
        layout.addWidget(self.go_btn)
        layout.addWidget(self.reg_btn)

    def login(self):  # Войти
        if self.username_lineEdit.text().strip() != "" and \
                not ("'" in self.username_lineEdit.text()):
            if authorization.find_in_db(self.username_lineEdit.text().strip()):
                self.handle_password_log_in()
            else:
                QMessageBox.warning(self, "Error", "Такого пользователя нет")
        else:
            QMessageBox.warning(
                self, 'Error', 'Имя не может быть пустым или содержать кавычки')

    def handle_password_registrate(self):  # Проверка пароля при регистрации
        if authorization.is_ok_passwd(self.password_lineEdit.text().strip()):
            if not authorization.find_in_db(self.username_lineEdit.text().strip()):
                authorization.add_in_db(self.username_lineEdit.text().strip(),
                                        self.password_lineEdit.text().strip())
                self.accept()
            else:
                QMessageBox.warning(
                    self, 'Error', 'Такой пользователь уже есть')
        else:
            QMessageBox.warning(self, "Error",
                                "Пароль должен быть > 6 букв, содержать заглавные буквы и цифры")

    def handle_password_log_in(self):  # Проверка пароля при входе
        if authorization.find_in_db(self.username_lineEdit.text().strip()) and \
                authorization.login_in_db(self.username_lineEdit.text().strip(),
                                          self.password_lineEdit.text().strip()):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Неверный пароль или несуществующий логин")

    def registrate(self):  # Регистрация
        if self.username_lineEdit.text().strip() != "" and \
                not ("'" in self.username_lineEdit.text()):
            if not authorization.find_in_db(self.username_lineEdit.text().strip()):
                self.handle_password_registrate()
            else:
                QMessageBox.warning(self, "Error", "Такой логин уже существует")
        else:
            QMessageBox.warning(self, "Error", "Имя не может быть пустым или содержать кавычки")
