import sys
import widgets

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog


if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    login = widgets.Login()

    if login.exec_() == QDialog.Accepted:
        window = widgets.MainWindow()
        window.show()
        sys.exit(app.exec_())
