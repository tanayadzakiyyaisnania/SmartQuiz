import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from utils import resource_path #Mengimpor fungsi resource_path
from menu import MenuWindow   #Mengimpor class MenuWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName("SmartQuiz") #Memberi nama aplikasi

    app.setWindowIcon(QIcon(resource_path("icon.ico"))) #Mengatur icon aplikasi

    window = MenuWindow()

    sys.exit(app.exec())
