from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QApplication
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap, QIcon
from utils import resource_path
from db import init_local_db
import os


class SiswaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_local_db()

        # LOAD UI
        loader = QUiLoader()
        file = QFile(resource_path("ui/siswa.ui")) # Membuka file siswa.ui

        ui = loader.load(file, self)  # Memuat UI dan menjadikan QMainWindow
        file.close()  # Menutup file UI setelah dimuat

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) # Mengatur central widget dari file UI
        self.setWindowTitle("SmartQuiz")    # Mengatur judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  # Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap

        central = self.centralWidget() # Mengambil central widget untuk background

        # BACKGROUND
        bg = central.findChild(QLabel, "bgLabel") # Mencari QLabel background dengan objectName bgLabel
        if bg:
            # Menampilkan gambar background pada QLabel
            bg.setPixmap(QPixmap(resource_path("images/wallMenu.png")))
            # Menyesuaikan ukuran gambar dengan ukuran QLabel
            bg.setScaledContents(True)
            # Menempatkan background di lapisan paling belakang
            bg.lower()

        # LOGO & ICON KATEGORI
        icons = {
            "logoLabel": "images/logoKuis.png",
            "iconLiterasi": "images/icon_literasi.png",
            "iconMatematika": "images/icon_mtk.png",
            "iconBahasa": "images/icon_bahasa.png",
            "iconUmum": "images/icon_umum.png",
            "iconKembali": "images/icon_home.png",
        }

        for obj_name, img_path in icons.items():
            lbl = self.findChild(QLabel, obj_name) # Mencari QLabel berdasarkan objectName
            if lbl and os.path.exists(resource_path(img_path)):
                lbl.setPixmap(QPixmap(resource_path(img_path))) # Menampilkan gambar pada QLabel
                lbl.setScaledContents(True) # Menyesuaikan ukuran gambar dengan QLabel

        # TOMBOL
        btn_literasi = self.findChild(QPushButton, "btnLiterasi")
        btn_mtk = self.findChild(QPushButton, "btnMatematika")
        btn_bahasa = self.findChild(QPushButton, "btnBahasa")
        btn_umum = self.findChild(QPushButton, "btnUmum")
        btn_kembali = self.findChild(QPushButton, "btnKembali")

        if btn_literasi:
            btn_literasi.clicked.connect(
                lambda: self.mulai_kuis("Literasi Dasar") # Mulai kuis kategori literasi
            )

        if btn_mtk:
            btn_mtk.clicked.connect(
                lambda: self.mulai_kuis("Matematika") # Mulai kuis matematika
            )

        if btn_bahasa:
            btn_bahasa.clicked.connect(
                lambda: self.mulai_kuis("Bahasa Indonesia") # Mulai kuis bahasa Indonesia
            )

        if btn_umum:
            btn_umum.clicked.connect(
                lambda: self.mulai_kuis("Pengetahuan Umum") # Mulai kuis pengetahuan umum
            )

        if btn_kembali:
            btn_kembali.clicked.connect(self.kembali_menu) # Kembali ke menu utama

        # TAMPILKAN WINDOW 
        self.show()

    # MULAI KUIS
    def mulai_kuis(self, kategori):
        from soal import SoalWindow
        self.soal = SoalWindow(kategori)
        self.close()

    # KEMBALI KE MENU
    def kembali_menu(self):
        from menu import MenuWindow
        self.menu = MenuWindow()
        self.close()
