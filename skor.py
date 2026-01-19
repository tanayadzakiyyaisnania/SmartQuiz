import random
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QWidget
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap, QIcon
from utils import resource_path
from db import insert_riwayat


class SkorWindow(QMainWindow):
    def __init__(self, kategori, skor):
        super().__init__()

        # LOAD UI
        loader = QUiLoader()
        file = QFile(resource_path("ui/skor.ui")) # Membuka file skor.ui

        ui = loader.load(file, self)  # Memuat UI dan menjadikan QMainWindow
        file.close()  # Menutup file UI setelah dimuat

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) # Mengatur central widget dari file UI
        self.setWindowTitle("SmartQuiz")    # Mengatur judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  # Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap

        central = self.centralWidget() # Mengambil central widget

        # LOGO
        lbl_logo = self.findChild(QLabel, "lblLogo") # Mencari QLabel logo berdasarkan objectName lblLogo
        if lbl_logo:
            lbl_logo.setPixmap(QPixmap(resource_path("images/logoKuis.png"))) # Menampilkan gambar logo pada QLabel
            lbl_logo.setScaledContents(True) # Menyesuaikan ukuran logo dengan ukuran QLabel

        # BACKGROUND
        bg_label = central.findChild(QLabel, "bgLabel") # Mencari QLabel background
        if bg_label:
            bg_label.setPixmap(QPixmap(resource_path("images/wall.png"))) # Menampilkan gambar background
            bg_label.setScaledContents(True) # Menyesuaikan ukuran background dengan QLabel
            bg_label.lower()  # Menempatkan background di lapisan paling belakang

        # PANEL SKOR
        panel = central.findChild(QWidget, "panelSkor") # Mencari objectname panelSkor
        if panel:
            # Mengatur warna latar dan sudut panel skor
            panel.setStyleSheet("""
            QWidget#panelSkor {
                background-color: #F8F8F0;
                border-radius: 20px;
            }
            """)

        # WIDGET DATA
        # Label untuk menampilkan skor
        self.lbl_skor = central.findChild(QLabel, "lblSkor")
        # Label untuk menampilkan pesan motivasi
        self.lbl_pesan = central.findChild(QLabel, "lblPesan")
        # Tombol untuk mengulangi kuis
        self.btn_ulangi = central.findChild(QPushButton, "btnUlangi")
        # Tombol untuk kembali ke menu utama
        self.btn_menu = central.findChild(QPushButton, "btnMenu")

        # DATA
        # Menyimpan kategori kuis
        self.kategori = kategori
        # Menyimpan kategori kuis
        self.skor = skor
        # Jumlah total soal kuis
        self.total_soal = 10

        # TAMPILKAN DATA
        # Menampilkan skor ke label
        if self.lbl_skor:
            self.lbl_skor.setText(
                f"Skor Kamu: {self.skor} / {self.total_soal}"
            )
        # Menampilkan pesan motivasi sesuai skor
        if self.lbl_pesan:
            self.lbl_pesan.setText(self.get_pesan())

        # SIMPAN RIWAYAT 
        insert_riwayat(self.kategori, self.skor, self.total_soal)

        # KONEKSI TOMBOL
        if self.btn_ulangi:
            self.btn_ulangi.clicked.connect(self.ulangi)

        if self.btn_menu:
            self.btn_menu.clicked.connect(self.ke_menu)

        self.show()

    # PESAN MOTIVASI
    def get_pesan(self):
        # Daftar pesan motivasi untuk skor rendah
        pesan_rendah = [
            "Tetap semangat! 💪\nBelajar itu proses.\nAyo coba lagi!",
            "Jangan menyerah 😊\nSedikit lagi kamu bisa!",
            "Tidak apa-apa salah 😉\nYang penting terus belajar!",
            "Kamu pasti bisa 🔥\nFokus sedikit lagi!"
        ]
        # Daftar pesan motivasi untuk skor tinggi
        pesan_tinggi = [
            "Hebat! 🎉\nPemahamanmu sangat baik!",
            "Luar biasa 👏\nTerus pertahankan prestasimu!",
            "Kerja bagus ⭐\nTerus tingkatkan kemampuanmu!",
            "Mantap! 🔥\nTerus belajar dan berkembang!"
        ]
        # Memilih pesan secara acak sesuai kategori skor > 7 dapat pesan rendah
        if self.skor <= 6:
            return random.choice(pesan_rendah)
        else:
            return random.choice(pesan_tinggi)

    # ULANGI KUIS
    def ulangi(self):
        from siswa import SiswaWindow
        self.siswa = SiswaWindow()
        self.close()

    # KE MENU
    def ke_menu(self):
        from menu import MenuWindow
        self.menu = MenuWindow()
        self.close()
