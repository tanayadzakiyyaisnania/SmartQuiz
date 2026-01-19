import sys
import os

# Untuk mendapatkan path absolut file resource
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # Saat sudah jadi EXE
        base_path = sys._MEIPASS  # Folder sementara tempat resource diekstrak
    else:
        # Saat run python biasa (pakai lokasi file ini)
        base_path = os.path.dirname(os.path.abspath(__file__))
    # Menggabungkan base_path dengan nama file resource
    return os.path.join(base_path, relative_path)