import os
import shutil
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QWidget,
    QLabel
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon, QPixmap
from db import insert_soal_guru, APP_DIR
from utils import resource_path


class GuruWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # LOAD UI
        loader = QUiLoader()
        file = QFile(resource_path("ui/guru.ui"))  # Membuka file guru.ui

        ui = loader.load(file, self)  # Memuat UI dan menjadikan QMainWindow
        file.close()  # Menutup file UI setelah dimuat

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) # Mengatur central widget dari file UI
        self.setWindowTitle("SmartQuiz")    # Mengatur judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  # Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap

        central = self.centralWidget() # Mengambil central widget untuk background

        # BACKGROUND
        bg_label = central.findChild(QLabel, "bgLabel") # Mencari QLabel background dengan objectName bgLabel
        if bg_label:
            # Menampilkan gambar background pada QLabel
            bg_label.setPixmap(QPixmap(resource_path("images/wall.png")))
            # Menyesuaikan ukuran gambar dengan ukuran QLabel
            bg_label.setScaledContents(True)
            # Menempatkan background di lapisan paling belakang
            bg_label.lower()

        # PANEL GURU
        guru_panel = central.findChild(QWidget, "guruPanel") # Mencari panel guru berdasarkan objectName guruPanel
        if guru_panel:
             # Mengatur warna latar dan sudut membulat panel guru
            guru_panel.setStyleSheet("""
            QWidget#guruPanel {
                background-color: #F8F8F0;
                border-radius: 20px;
            }
            """)

        # KONEKSI TOMBOL
        self.btn_pilih = self.findChild(QWidget, "btnPilihGambar")
        self.btn_simpan = self.findChild(QWidget, "btnSimpan")
        self.btn_baru = self.findChild(QWidget, "btnBaru")
        self.btn_kembali = self.findChild(QWidget, "btnKembali")
        self.btn_lihat = self.findChild(QWidget, "btnLihat")

        if self.btn_pilih:
            self.btn_pilih.clicked.connect(self.pilih_gambar) # Buka dialog pilih gambar
        if self.btn_simpan:
            self.btn_simpan.clicked.connect(self.simpan_soal) # Simpan soal ke database
        if self.btn_baru:
            self.btn_baru.clicked.connect(self.reset_form) # Reset semua input form
        if self.btn_kembali:
            self.btn_kembali.clicked.connect(self.kembali_menu) # Kembali ke menu utama
        if self.btn_lihat:
            self.btn_lihat.clicked.connect(self.lihat_soal) #lihat soal berdasarkan kategori

        # TAMPILKAN WINDOW
        self.show()

    # UNTUK MEMILIH GAMBAR SOAL
    def pilih_gambar(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih Gambar Soal",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )

        if not file_path:
            return

        nama_file = os.path.basename(file_path) # Mengambil nama file dari path

        folder_soal = os.path.join(APP_DIR, "images", "soal") # Menentukan folder penyimpanan gambar soal(Quiz_local.db)
        os.makedirs(folder_soal, exist_ok=True) # Membuat folder jika belum ada

        tujuan = os.path.join(folder_soal, nama_file) # Menentukan path tujuan file
        shutil.copy(file_path, tujuan) # Menyalin file gambar ke folder soal

         # Menyimpan path gambar ke input teks
        self.findChild(QWidget, "txtGambar").setText(
            f"images/soal/{nama_file}"
        )

    # AMBIL JAWABAN BENAR
    def get_jawaban_benar(self):
        if self.findChild(QWidget, "rbA").isChecked():
            return "A"
        if self.findChild(QWidget, "rbB").isChecked():
            return "B"
        if self.findChild(QWidget, "rbC").isChecked():
            return "C"
        if self.findChild(QWidget, "rbD").isChecked():
            return "D"
        return None

    # SIMPAN SOAL
    def simpan_soal(self):
        # Mengambil kategori soal
        kategori = self.findChild(QWidget, "cmbKategori").currentText().strip()
        # Mengambil teks pertanyaan
        pertanyaan = self.findChild(QWidget, "txtPertanyaan").toPlainText().strip()
        # Mengambil opsi jawaban A–D
        opsi_a = self.findChild(QWidget, "txtA").text().strip()
        opsi_b = self.findChild(QWidget, "txtB").text().strip()
        opsi_c = self.findChild(QWidget, "txtC").text().strip()
        opsi_d = self.findChild(QWidget, "txtD").text().strip()
        # Mengambil jawaban benar
        jawaban_benar = self.get_jawaban_benar()

        # Mengambil path gambar (opsional)
        gambar = self.findChild(QWidget, "txtGambar").text().strip() or None

        # Validasi input wajib
        if not all([kategori, pertanyaan, opsi_a, opsi_b, opsi_c, opsi_d, jawaban_benar]):
            QMessageBox.warning(
                self,
                "Peringatan",
                "Semua field wajib diisi kecuali gambar!"
            )
            return
        # Konfirmasi sebelum menyimpan soal
        konfirmasi = QMessageBox.question(
            self,
            "Simpan Soal",
            "Yakin ingin menyimpan soal ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi != QMessageBox.Yes: # Jika tidak dikonfirmasi, batalkan
            return

        # Menyimpan data soal ke database
        insert_soal_guru(
            kategori, pertanyaan,
            opsi_a, opsi_b, opsi_c, opsi_d,
            jawaban_benar, gambar
        )

        # Menampilkan pesan berhasil
        QMessageBox.information(
            self,
            "Berhasil",
            "Soal berhasil ditambahkan!"
        )

        self.reset_form()  # Mengosongkan kembali form input

    # LIHAT SOAL
    def lihat_soal(self):
        from lihat_soal_guru import LihatSoalGuru
        kategori = self.findChild(QWidget, "cmbKategori").currentText().strip()
        self.window = LihatSoalGuru(kategori)

    # RESET FORM
    def reset_form(self):
        self.findChild(QWidget, "txtPertanyaan").clear()
        self.findChild(QWidget, "txtA").clear()
        self.findChild(QWidget, "txtB").clear()
        self.findChild(QWidget, "txtC").clear()
        self.findChild(QWidget, "txtD").clear()
        self.findChild(QWidget, "txtGambar").clear()
        # Mengosongkan semua radio button
        for rb in ("rbA", "rbB", "rbC", "rbD"):
            self.findChild(QWidget, rb).setChecked(False)

    # KEMBALI KE MENU
    def kembali_menu(self):
        from menu import MenuWindow
        self.menu = MenuWindow()
        self.close()
