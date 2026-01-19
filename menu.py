import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QMainWindow
)
from PySide6.QtUiTools import QUiLoader #Loader file .ui
from PySide6.QtCore import QFile #Membaca file
from PySide6.QtGui import QPixmap, QIcon
from utils import resource_path


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # LOAD UI
        loader = QUiLoader()
        ui_file = QFile(resource_path("ui/menu.ui")) #Membuka file menu.ui

        ui = loader.load(ui_file, self)  #Memuat UI ke dalam window
        ui_file.close() #Menutup file UI

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) #Mengatur widget utama dari file .ui
        self.setWindowTitle("SmartQuiz") #Judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  #Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap
 
        # BACKGROUND
        central = self.centralWidget() # Mengambil central widget untuk background
        bg_path = resource_path("images/wallMenu.png").replace("\\", "/") #Mengambil path gambar background dan menyesuaikan format path untuk stylesheet Qt

        #Mengatur gambar sebagai background, background hanya muncul sekali, dan Background di tengah
        central.setStyleSheet(f"""
        QWidget#centralwidget {{
            background-image: url("{bg_path}"); 
            background-repeat: no-repeat;   
            background-position: center;  
        }}
        """)

        # LOGO
        logo_path = resource_path("images/logoKuis.png") #Mengambil path gambar logo
        logo_label = central.findChild(QLabel, "logoLabel") #Mencari QLabel dengan objectName "logoLabel" dari file UI

        if logo_label:
            pixmap = QPixmap(logo_path) #Memuat gambar logo ke objek QPixmap
            if not pixmap.isNull(): #Mengecek apakah gambar berhasil dimuat
                logo_label.setPixmap(pixmap) #Menampilkan gambar logo pada QLabel
                logo_label.setScaledContents(True) #Ukuran gambar ikut ukuran label

        # BUTTON
        # Mencari tombol siswa berdasarkan objectName btnSiswa di file UI
        btn_siswa = central.findChild(QPushButton, "btnSiswa")
        # Mencari tombol guru berdasarkan objectName btnGuru
        btn_guru = central.findChild(QPushButton, "btnGuru")
        # Mencari tombol riwayat berdasarkan objectName btnRiwayat
        btn_riwayat = central.findChild(QPushButton, "btnRiwayat")
        # Mencari tombol keluar berdasarkan objectName btnKeluar
        btn_keluar = central.findChild(QPushButton, "btnKeluar")

        if btn_siswa: # Mengecek apakah tombol siswa ditemukan
            btn_siswa.clicked.connect(self.ke_siswa) # Menghubungkan klik tombol ke fungsi ke_siswa()

        if btn_guru:# Mengecek apakah tombol guru ditemukan
            btn_guru.clicked.connect(self.ke_guru) # Menghubungkan klik tombol ke fungsi ke_guru()

        if btn_riwayat: # Mengecek apakah tombol riwayat ditemukan
            btn_riwayat.clicked.connect(self.ke_riwayat) # Menghubungkan klik tombol ke fungsi ke_riwayat()

        if btn_keluar: # Mengecek apakah tombol keluar ditemukan
            btn_keluar.clicked.connect(QApplication.quit)  # Menghubungkan klik tombol untuk keluar dari aplikasi


        self.show() # Menampilkan window menu utama

    # Berpindah
    def ke_siswa(self): # Berpindah ke halaman siswa
        from siswa import SiswaWindow
        self.siswa = SiswaWindow()
        self.close()

    def ke_guru(self): # Berpindah ke halaman guru
        from guru import GuruWindow
        self.guru = GuruWindow()
        self.close()

    def ke_riwayat(self): # Berpindah ke halaman riwayat
        from riwayat import RiwayatWindow
        self.riwayat = RiwayatWindow()
        self.close()