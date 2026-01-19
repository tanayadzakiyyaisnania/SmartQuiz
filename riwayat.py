from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
    QLabel,
    QWidget,
    QPushButton,
    QTableWidget
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QIcon, QPixmap
from db import get_riwayat, delete_riwayat_by_id
from utils import resource_path


class RiwayatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # LOAD UI
        loader = QUiLoader()
        file = QFile(resource_path("ui/riwayat.ui"))# Membuka file riwayat.ui

        ui = loader.load(file, self)  # Memuat UI dan menjadikan QMainWindow
        file.close()  # Menutup file UI setelah dimuat

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) # Mengatur central widget dari file UI
        self.setWindowTitle("SmartQuiz")    # Mengatur judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  # Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap

        central = self.centralWidget() # Mengambil central widget

        # BACKGROUND
        bg_label = central.findChild(QLabel, "bgLabel") # Mencari QLabel background berdasarkan objectName bgLabel
        if bg_label:
            # Menampilkan gambar background
            bg_label.setPixmap(QPixmap(resource_path("images/wall.png")))
            # Menyesuaikan ukuran gambar dengan ukuran QLabel
            bg_label.setScaledContents(True)
            # Menempatkan background di lapisan paling belakang
            bg_label.lower()

        # PANEL RIWAYAT
        panel = central.findChild(QWidget, "panelRiwayat") # Mencari objectname panelRiwayat
        if panel:
            # Mengatur warna latar dan sudut panel riwayat
            panel.setStyleSheet("""
            QWidget#panelRiwayat {
                background-color: #F8F8F0;
                border-radius: 20px;
            }
            """)

        # TABLE
        self.table = self.findChild(QTableWidget, "tableWidget")

        self.table.setColumnCount(5) # Menentukan jumlah kolom tabel
        # Menentukan judul kolom tabel
        self.table.setHorizontalHeaderLabels(
            ["No", "Kategori", "Tanggal", "Skor", "Total Soal"]
        )
        # Seleksi data per baris
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Hanya satu baris yang bisa dipilih
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        # Menonaktifkan edit manual pada tabel
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Menyembunyikan header vertikal
        self.table.verticalHeader().setVisible(False)

        # Lebar kolom menyesuaikan ukuran tabel
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # TOMBOL
        self.btn_hapus = self.findChild(QPushButton, "btnHapusRiwayat")
        self.btn_kembali = self.findChild(QPushButton, "btnKembali")

        if self.btn_hapus:
            self.btn_hapus.clicked.connect(self.hapus_riwayat)

        if self.btn_kembali:
            self.btn_kembali.clicked.connect(self.kembali_menu)


        self.load_data()

        # SHOW
        self.show()

    def load_data(self):
        data = get_riwayat()  # (id, kategori, tanggal, skor, total_soal)
        self.table.setRowCount(len(data)) # Menentukan jumlah baris tabel

        # Mengambil data riwayat per baris
        for row, item in enumerate(data):
            riwayat_id, kategori, tanggal, skor, total = item

            no_item = QTableWidgetItem(str(row + 1)) # Membuat nomor urut riwayat
            no_item.setFlags(no_item.flags() & ~Qt.ItemIsEditable) # Menonaktifkan edit pada kolom nomor
            no_item.setData(Qt.UserRole, riwayat_id) # Menyimpan ID riwayat secara tersembunyi

            # Mengisi data ke tabel
            self.table.setItem(row, 0, no_item)
            self.table.setItem(row, 1, QTableWidgetItem(kategori))
            self.table.setItem(row, 2, QTableWidgetItem(tanggal))
            self.table.setItem(row, 3, QTableWidgetItem(str(skor)))
            self.table.setItem(row, 4, QTableWidgetItem(str(total)))
        # Menyesuaikan tinggi baris dengan isi tabel
        self.table.resizeRowsToContents()

    # HAPUS RIWAYAT
    def hapus_riwayat(self):
        row = self.table.currentRow() # Mengambil baris yang sedang dipilih
        # Validasi jika belum memilih data
        if row < 0:
            QMessageBox.information(
                self,
                "Info",
                "Pilih satu riwayat terlebih dahulu"
            )
            return
        # Mengambil ID riwayat dari data tersembunyi
        riwayat_id = self.table.item(row, 0).data(Qt.UserRole)
        # Validasi jika ingin menghapus riwayat
        if QMessageBox.question(
            self,
            "Hapus Riwayat",
            "Yakin ingin menghapus riwayat ini?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            delete_riwayat_by_id(riwayat_id) # Menghapus riwayat dari database
            self.load_data()  # Memuat ulang tabel

    def kembali_menu(self):
        from menu import MenuWindow
        self.menu = MenuWindow()
        self.close()