from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QPixmap, QIcon
from db import get_soal_guru, delete_soal_by_id
from utils import resource_path


class LihatSoalGuru(QMainWindow):
    def __init__(self, kategori):
        super().__init__()

        # LOAD UI
        loader = QUiLoader()
        file = QFile(resource_path("ui/soal_guru.ui")) # Membuka file soal_guru.ui

        ui = loader.load(file, self)  # Memuat UI dan menjadikan QMainWindow
        file.close()  # Menutup file UI setelah dimuat

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) # Mengatur central widget dari file UI
        self.setWindowTitle("SmartQuiz")    # Mengatur judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  # Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap

        central = self.centralWidget() # Mengambil central widget 

        # BACKGROUND
        bg_label = central.findChild(QLabel, "bgLabel") # Mencari QLabel background dengan objectName bgLabel
        if bg_label:
            # Menampilkan gambar background pada QLabel
            bg_label.setPixmap(QPixmap(resource_path("images/wall.png")))
            # Menyesuaikan ukuran gambar dengan ukuran QLabel
            bg_label.setScaledContents(True)
            # Menempatkan background di lapisan paling belakang
            bg_label.lower()

        # PANEL
        panel = central.findChild(QWidget, "panelLihat") # Mencari object panelLihat
        if panel:
             # Mengatur warna dan sudut panel
            panel.setStyleSheet("""
            QWidget#panelLihat {
                background-color: #F8F8F0;
                border-radius: 20px;
            }
            """)

        # DATA
        self.kategori = kategori  # Menyimpan kategori soal yang sudah dibuat guru

        # WIDGET
        # Tabel untuk menampilkan soal
        self.table = self.findChild(QTableWidget, "tableSoal")
        # Tombol hapus soal
        self.btn_hapus = self.findChild(QPushButton, "btnHapusSoal")
        # Tombol kembali ke halaman guru
        self.btn_kembali = self.findChild(QPushButton, "btnKembaliGuru")

        # SETUP TABLE
        self.table.setColumnCount(4) # Menentukan jumlah kolom tabel
         # Menentukan judul kolom tabel
        self.table.setHorizontalHeaderLabels(
            ["No", "Pertanyaan", "Kategori", "Jawaban"]
        )

        # Seleksi per baris
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Menonaktifkan edit manual ditabel
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Menyembunyikan header vertikal
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        # Lebar kolom menyesuaikan ukuran tabel
        header.setSectionResizeMode(QHeaderView.Stretch)

        # SIGNAL
        if self.btn_hapus:
            self.btn_hapus.clicked.connect(self.hapus_soal)

        if self.btn_kembali:
            self.btn_kembali.clicked.connect(self.kembali_ke_guru)

        # LOAD DATA
        self.load_data()

        # SHOW
        self.show()

    def load_data(self):
        # Mengambil data soal berdasarkan kategori
        data = get_soal_guru(self.kategori)
        # Menentukan jumlah baris tabel
        self.table.setRowCount(len(data))
        # Mengambil ID, pertanyaan, dan jawaban dari data
        for row, soal in enumerate(data):
            soal_id, pertanyaan, *_ , jawaban, _ = soal

            no_item = QTableWidgetItem(str(row + 1)) # Nomor urut soal
            no_item.setData(Qt.UserRole, soal_id)  # simpan ID tersembunyi
            no_item.setFlags(no_item.flags() & ~Qt.ItemIsEditable) # Menonaktifkan edit pada kolom nomor

            # Mengisi data ke tabel
            self.table.setItem(row, 0, no_item)
            self.table.setItem(row, 1, QTableWidgetItem(pertanyaan))
            self.table.setItem(row, 2, QTableWidgetItem(self.kategori))
            self.table.setItem(row, 3, QTableWidgetItem(jawaban))
        # Menyesuaikan tinggi baris dengan isi
        self.table.resizeRowsToContents()

    # HAPUS SOAL
    def hapus_soal(self):
        row = self.table.currentRow() # Mengambil baris yang dipilih

        # Validasi jika belum memilih bariS
        if row < 0:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Pilih soal yang ingin dihapus"
            )
            return
        # Mengambil ID soal dari data tersembunyi
        soal_id = self.table.item(row, 0).data(Qt.UserRole)

        # Validasi jika ingin menghapus soal
        if QMessageBox.question(
            self,
            "Hapus Soal",
            "Yakin ingin menghapus soal ini?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            delete_soal_by_id(soal_id) # Menghapus soal dari database
            self.load_data() # Memuat ulang data tabel

    # =========================
    def kembali_ke_guru(self):
        from guru import GuruWindow
        self.guru = GuruWindow()
        self.close()
