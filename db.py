import sqlite3
from datetime import datetime
import random
import os
import sys

# BASE DIR (PYTHON & .EXE)
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS # Folder sementara (EXE)
    return os.path.dirname(os.path.abspath(__file__))  # Folder file Python saat run 

BASE_DIR = get_base_dir() #Menyimpan folder dasar aplikasi

# DB DEFAULT (READ-ONLY, DALAM EXE)
DEFAULT_DB = os.path.join(BASE_DIR, "quiz.db") # Path database bawaan aplikasi

# APP DIR (WRITEABLE - USER)
APP_DIR = os.path.join(os.path.expanduser("~"), "SmartQuiz") # Folder aplikasi di home user
os.makedirs(APP_DIR, exist_ok=True) # Membuat folder jika belum ada

# Path database lokal (guru & riwayat)
LOCAL_DB = os.path.join(APP_DIR, "quiz_local.db")

# KONEKSI
def get_default_conn():
    return sqlite3.connect(DEFAULT_DB) # Koneksi ke database default

def get_local_conn():
    return sqlite3.connect(LOCAL_DB) # Koneksi ke database lokal

# INIT DB LOKAL (GURU + RIWAYAT)
def init_local_db():
    conn = get_local_conn() # Membuka koneksi database lokal
    cur = conn.cursor()  # Membuat cursor SQL
    # Membuat tabel soal guru jika belum ada
    cur.execute("""
        CREATE TABLE IF NOT EXISTS soal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT,
            pertanyaan TEXT,
            opsi_a TEXT,
            opsi_b TEXT,
            opsi_c TEXT,
            opsi_d TEXT,
            jawaban_benar TEXT,
            gambar TEXT,
            dibuat_oleh TEXT
        )
    """)
     # Membuat tabel riwayat kuis
    cur.execute("""
        CREATE TABLE IF NOT EXISTS riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT,
            tanggal TEXT,
            skor INTEGER,
            total_soal INTEGER
        )
    """)

    conn.commit() # Menyimpan perubahan
    conn.close() # Menutup koneksi

# AMBIL SOAL DEFAULT (GLOBAL)
def get_soal_default(kategori):
    conn = get_default_conn() # Koneksi ke DB default
    cur = conn.cursor() # Cursor SQL
    # Ambil soal berdasarkan kategori (case-insensitive)
    cur.execute("""
        SELECT id, pertanyaan, opsi_a, opsi_b, opsi_c, opsi_d,
               jawaban_benar, gambar
        FROM soal
        WHERE TRIM(LOWER(kategori)) = TRIM(LOWER(?))
    """, (kategori,))

    data = cur.fetchall() # Ambil semua hasil query
    conn.close()       # Tutup koneksi
    return data     ## Kembalikan data soal

# AMBIL SOAL GURU (LOKAL)
def get_soal_guru(kategori):
    conn = get_local_conn() # Koneksi ke DB lokal
    cur = conn.cursor()      # Cursor SQL
    # Ambil soal buatan guru
    cur.execute("""
        SELECT id, pertanyaan, opsi_a, opsi_b, opsi_c, opsi_d,
               jawaban_benar, gambar
        FROM soal
        WHERE TRIM(LOWER(kategori)) = TRIM(LOWER(?))
          AND dibuat_oleh = 'guru'
    """, (kategori,))

    data = cur.fetchall() # Ambil data
    conn.close()    # Tutup koneksi
    return data # Kembalikan data

# GABUNG SOAL (UNTUK KUIS)
def get_soal_by_kategori(kategori, jumlah=10):
    # Ambil soal guru & default
    soal_guru = get_soal_guru(kategori)
    soal_default = get_soal_default(kategori)
    # Acak urutan soal
    random.shuffle(soal_guru)
    random.shuffle(soal_default)

    hasil = [] # List hasil soal kuis

    # Masukkan soal guru 
    for s in soal_guru:
        if len(hasil) < jumlah:
            hasil.append(s)
    # Tambahkan soal default jika masih kurang
    for s in soal_default:
        if len(hasil) < jumlah:
            hasil.append(s)

    return hasil  # Kembalikan daftar soal kuis

# INSERT SOAL GURU (LOKAL)
def insert_soal_guru(
    kategori, pertanyaan,
    opsi_a, opsi_b, opsi_c, opsi_d,
    jawaban_benar, gambar=None
):
    conn = get_local_conn() # Koneksi DB lokal
    cur = conn.cursor() # Cursor SQL
    # Simpan soal guru
    cur.execute("""
        INSERT INTO soal
        (kategori, pertanyaan, opsi_a, opsi_b, opsi_c, opsi_d,
         jawaban_benar, gambar, dibuat_oleh)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'guru')
    """, (
        kategori, pertanyaan,
        opsi_a, opsi_b, opsi_c, opsi_d,
        jawaban_benar, gambar
    ))

    conn.commit() # Simpan perubahan
    conn.close()  # Tutup koneksi

# HAPUS SOAL GURU
def delete_soal_by_id(soal_id):
    conn = get_local_conn() # Koneksi DB lokal
    cur = conn.cursor() # Cursor SQL
    # Hapus soal guru berdasarkan ID
    cur.execute(
        "DELETE FROM soal WHERE id = ? AND dibuat_oleh = 'guru'",
        (soal_id,)
    )

    conn.commit() # Simpan perubahan
    conn.close()  # Tutup koneksi

# RIWAYAT
def insert_riwayat(kategori, skor, total_soal):
    conn = get_local_conn() # Koneksi DB lokal
    cur = conn.cursor() # Cursor SQL

    # Ambil tanggal & waktu sekarang
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Simpan riwayat kuis
    cur.execute("""
        INSERT INTO riwayat
        (kategori, tanggal, skor, total_soal)
        VALUES (?, ?, ?, ?)
    """, (kategori, tanggal, skor, total_soal))

    conn.commit() # Simpan perubahan
    conn.close() # Tutup koneksi

def get_riwayat():
    conn = get_local_conn()  # Koneksi DB lokal
    cur = conn.cursor() # Cursor SQL
     # Ambil semua riwayat
    cur.execute("""
        SELECT id, kategori, tanggal, skor, total_soal
        FROM riwayat
        ORDER BY id ASC
    """)

    data = cur.fetchall() # Ambil data
    conn.close() # Tutup koneksi
    return data # Kembalikan riwayat

def delete_riwayat_by_id(riwayat_id):
    conn = get_local_conn() # Koneksi DB lokal
    cur = conn.cursor() # Cursor SQL
    # Hapus riwayat berdasarkan ID
    cur.execute(
        "DELETE FROM riwayat WHERE id = ?",
        (riwayat_id,)
    )

    conn.commit() # Simpan perubahan
    conn.close() # Tutup koneksi