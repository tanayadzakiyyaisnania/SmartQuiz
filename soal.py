import os
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox,
    QLabel, QPushButton, QRadioButton,
    QScrollArea, QWidget
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile
from PySide6.QtGui import QPixmap, QIcon
from db import get_soal_by_kategori, APP_DIR
from utils import resource_path


class SoalWindow(QMainWindow):
    def __init__(self, kategori):
        super().__init__()

        # LOAD UI
        loader = QUiLoader()
        file = QFile(resource_path("ui/soal.ui")) # Membuka file riwayat.ui

        ui = loader.load(file, self)  # Memuat UI dan menjadikan QMainWindow
        file.close()  # Menutup file UI setelah dimuat

        # SET WINDOW UTAMA
        self.setCentralWidget(ui.centralWidget()) # Mengatur central widget dari file UI
        self.setWindowTitle("SmartQuiz")    # Mengatur judul window
        self.setWindowIcon(QIcon(resource_path("icon.ico")))  # Mengatur icon aplikasi
        self.setFixedSize(1000, 600) # Ukuran window tetap

        self.central = self.centralWidget() # Mengambil central widget

        # OPSI PANEL DAN SCROLL
        self.opsiPanel = self.central.findChild(QWidget, "opsiPanel") # Mencari objectname opsiPanel 
        # Membuat QScrollArea sebagai wadah panel soal
        self.scrollArea = QScrollArea(self.central)
        # Isi scroll menyesuaikan ukuran area
        self.scrollArea.setWidgetResizable(True)
        # Menyamakan posisi dan ukuran scroll dengan panel asli
        self.scrollArea.setGeometry(self.opsiPanel.geometry())
        # Melepaskan opsiPanel dari parent lama
        self.opsiPanel.setParent(None)
        # Memasukkan opsiPanel ke dalam scroll area
        self.scrollArea.setWidget(self.opsiPanel)

        # WIDGET
        self.lbl_nomor = self.opsiPanel.findChild(QLabel, "lblNomor") # Label nomor soal
        self.lbl_pertanyaan = self.opsiPanel.findChild(QLabel, "lblPertanyaan") # Label teks pertanyaan
        self.lbl_gambar = self.opsiPanel.findChild(QLabel, "lblGambarSoal") # Gambar soal
        self.lbl_benar = self.opsiPanel.findChild(QLabel, "lblBenar") # Label benar / salah
        # Radio button opsi jawaban A–D
        self.rbA = self.opsiPanel.findChild(QRadioButton, "rbA")
        self.rbB = self.opsiPanel.findChild(QRadioButton, "rbB")
        self.rbC = self.opsiPanel.findChild(QRadioButton, "rbC")
        self.rbD = self.opsiPanel.findChild(QRadioButton, "rbD")
        # Tombol next dan back
        self.btn_next = self.central.findChild(QPushButton, "btnNext")
        self.btn_back = self.central.findChild(QPushButton, "btnBack")

        # DATA
        self.kategori = kategori # Menyimpan kategori kuis
        # Mengambil daftar soal berdasarkan kategori (maks 10 soal)
        self.soal_list = get_soal_by_kategori(kategori, 10)
        self.index = 0 # Index soal yang sedang ditampilkan

        # Menyimpan jawaban user untuk setiap soal
        self.jawaban_user = [None] * len(self.soal_list)
        # Penanda apakah soal sudah dicek 
        self.sudah_dicek = [False] * len(self.soal_list)
        # Jawaban yang sedang dipilih user
        self.current_checked = None

        # SIGNAL
        # Menyimpan pilihan jawaban saat radio button dipilih
        self.rbA.toggled.connect(lambda v: self.set_checked("A", v))
        self.rbB.toggled.connect(lambda v: self.set_checked("B", v))
        self.rbC.toggled.connect(lambda v: self.set_checked("C", v))
        self.rbD.toggled.connect(lambda v: self.set_checked("D", v))
        # Tombol next untuk Lanjut soal
        self.btn_next.clicked.connect(self.next_soal)
        # Tombol back untuk kembali ke soal sebelumnya
        self.btn_back.clicked.connect(self.kembali_soal)

        # TAMPILKAN SOAL PERTAMA
        self.tampilkan_soal()
        self.show()

    # Menyimpan opsi jawaban yang dipilih user
    def set_checked(self, value, checked):
        if checked:
            self.current_checked = value
    # Mengambil data soal sesuai index
    def tampilkan_soal(self):
        soal = self.soal_list[self.index]
        self.current_checked = None
        # Menampilkan nomor soal
        self.lbl_nomor.setText(
            f"Soal {self.index + 1} / {len(self.soal_list)}"
        )
        # Menampilkan teks pertanyaan
        self.lbl_pertanyaan.setText(
            soal[1].replace("\\n", "\n")
        )
        # Menampilkan opsi jawaban
        self.rbA.setText(soal[2])
        self.rbB.setText(soal[3])
        self.rbC.setText(soal[4])
        self.rbD.setText(soal[5])

        # reset radio
        for rb in (self.rbA, self.rbB, self.rbC, self.rbD):
            rb.setAutoExclusive(False)
            rb.setChecked(False)
            rb.setAutoExclusive(True)
            rb.setEnabled(True)

        # reset feedback
        self.lbl_benar.setText("")
        self.lbl_benar.setStyleSheet("")

        # GAMBAR
        gambar = soal[7] # Path gambar soal (jika ada)

        if gambar:
            # CASE 1: Soal dari guru (disimpan di APP_DIR)
            path_guru = os.path.join(APP_DIR, gambar)

            # CASE 2: Soal default (disimpan di resource)
            path_default = resource_path(
                gambar if gambar.startswith("images/") else f"images/soal/{gambar}"
            )
            # Menentukan path gambar yang valid
            if os.path.exists(path_guru):
                full_path = path_guru
            elif os.path.exists(path_default):
                full_path = path_default
            else:
                full_path = None
            # Menampilkan gambar soal
            if full_path:
                pixmap = QPixmap(full_path)
                self.lbl_gambar.setPixmap(pixmap)
                self.lbl_gambar.setScaledContents(True)
                self.lbl_gambar.setMaximumHeight(300)
                self.lbl_gambar.setAlignment(Qt.AlignCenter)
                self.lbl_gambar.setVisible(True)
    # Menyembunyikan label gambar jika tidak ada
            else:
                self.lbl_gambar.clear()
                self.lbl_gambar.setVisible(False)
        else:
            self.lbl_gambar.clear()
            self.lbl_gambar.setVisible(False)

        # Mengembalikan scroll ke posisi atas
        self.scrollArea.verticalScrollBar().setValue(0)

        # restore jawaban jika kembali
        if self.jawaban_user[self.index]:
            mapping = {
                "A": self.rbA,
                "B": self.rbB,
                "C": self.rbC,
                "D": self.rbD
            }
            # Menyalakan kembali radio button sesuai jawaban yang dulu dipilih user
            mapping[self.jawaban_user[self.index]].setChecked(True)
            # Menyimpan ulang jawaban
            self.current_checked = self.jawaban_user[self.index]
            # Soal pernah dicek, tulisan benar salah tidak hilang jika back
            if self.sudah_dicek[self.index]:
                self.tampilkan_feedback(self.soal_list[self.index][6])

    def tampilkan_feedback(self, jawaban_benar):
        # Ambil jawaban yang dipilih user di soal
        jawaban_user = self.jawaban_user[self.index]
        # Feedback jawaban benar
        if jawaban_user == jawaban_benar:
            self.lbl_benar.setText("✅ Jawaban Anda BENAR")
            self.lbl_benar.setStyleSheet(
                "color: green; font-weight: bold;"
            )
        else:
        # Feedback jawaban salah
            self.lbl_benar.setText(
                f"❌ Jawaban Anda SALAH\n"
                f"Jawaban yang benar adalah: {jawaban_benar}"
            )
            self.lbl_benar.setStyleSheet(
                "color: red; font-weight: bold;"
            )
        # Menonaktifkan opsi setelah dijawab
        for rb in (self.rbA, self.rbB, self.rbC, self.rbD):
            rb.setEnabled(False)

    def next_soal(self):
        # tahap 1: cek jawaban
        if not self.sudah_dicek[self.index]:
            # Validasi jika belum memilih jawaban
            if not self.current_checked:
                QMessageBox.warning(
                    self,
                    "Peringatan",
                    "Jawaban wajib diisi"
                )
                return
            # Simpan jawaban user dan ambil jawaban benar
            self.jawaban_user[self.index] = self.current_checked
            jawaban_benar = self.soal_list[self.index][6]
            # Tampilkan feedback benar atau salah lalu berhenti
            self.tampilkan_feedback(jawaban_benar)
            self.sudah_dicek[self.index] = True
            return

        # tahap 2: lanjut soal
        if self.index == len(self.soal_list) - 1:
            self.ke_skor()
            return

        self.index += 1
        self.tampilkan_soal()

    # Kembali ke soal sebelumnya
    def kembali_soal(self):
        if self.index > 0:
            self.index -= 1
            self.tampilkan_soal()
        else:
            # Jika di soal pertama - kembali ke menu siswa
            from siswa import SiswaWindow
            self.siswa = SiswaWindow()
            self.close()
    # Menghitung skor akhir
    def ke_skor(self):
        skor = 0
        # Menambah skor untuk setiap jawaban benar
        for i, jawaban in enumerate(self.jawaban_user):
            if jawaban == self.soal_list[i][6]:
                skor += 1

        from skor import SkorWindow
        self.skor_window = SkorWindow(self.kategori, skor)
        self.close()
