import sys
import widgets
import authorization

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    authorized = False

    app = QApplication(sys.argv)
    auth_window = widgets.AuthorizationWindow()
    auth_window.show()
    sys.exit(app.exec())
