# -------------------------- Sistem Validasi Registrasi Mahasiswa -------------------------- 
from abc import ABC, abstractmethod
import logging

# Konfigurasi dasar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Mahasiswa:
    """
    Model data Mahasiswa sederhana.
    Args:
        nim (str): Nomor Induk Mahasiswa.
        sks_diambil (int): Jumlah SKS yang diambil mahasiswa pada semester ini.
        matkul_prasyarat (bool): Status pemenuhan mata kuliah prasyarat.
    """
    def __init__(self, nim: str, sks_diambil: int, matkul_prasyarat: bool = True):
        self.nim = nim
        self.sks_diambil = sks_diambil
        self.matkul_prasyarat = matkul_prasyarat

# 2. Implementasi DIP/OCP: Abstraksi IValidationRule
class IValidationRule(ABC):
    """Abstraksi aturan validasi (Memenuhi DIP)"""
    @abstractmethod
    def validate(self, data: Mahasiswa) -> bool:
        """
        data (Mahasiswa): Objek mahasiswa yang akan divalidasi.
        Returns:
            bool: True jika validasi berhasil, False jika gagal.
        """
        pass

# 2. Implementasi DIP/OCP: Kelas Konkrit (Rules)
class SksLimitRule(IValidationRule):
    """Aturan validasi Batas SKS (Memenuhi SRP)."""
    SKS_LIMIT = 24
    def validate(self, data: Mahasiswa) -> bool:
        """
        Memeriksa apakah SKS yang diambil melebihi batas 24 SKS.
        """
        if data.sks_diambil > self.SKS_LIMIT:
            logging.warning(f"GAGAL : Batas SKS terlampaui ({data.sks_diambil} > {self.SKS_LIMIT}).")
            return False
        logging.info("SUKSES : Batas SKS terpenuhi.")
        return True

class PrerequisiteRule(IValidationRule):
    """Aturan validasi Prasyarat Mata Kuliah (Memenuhi SRP)."""
    def validate(self, data: Mahasiswa) -> bool:
        """Memeriksa status pemenuhan mata kuliah prasyarat."""
        if not data.matkul_prasyarat:
            logging.warning("GAGAL : Mata kuliah prasyarat belum dipenuhi.")
            return False
        logging.info("SUKSES : Prasyarat terpenuhi.")
        return True


# 3. Implementasi SRP: Kelas Koordinator
class RegistrationService:
    """
    Kelas layanan untuk mengkoordinasi (menjalankan) semua aturan validasi.
    Memenuhi SRP dan menerapkan Dependency Injection.
    """
    def __init__(self, validation_rules: list[IValidationRule]):
        """Inisiasi RegistrationService dengan menyuntikkan (inject) daftar aturan validasi.
        Args:
            validation_rules (list[IValidationRule]): Daftar aturan validasi yang akan dijalankan.
        """
        self.validation_rules = validation_rules

    def register_mhs(self, mhs: Mahasiswa) -> bool:
        """Menjalankan proses registrasi dengan mengiterasi semua aturan yang di-inject.
        Args:
            mhs (Mahasiswa): Objek Mahasiswa yang akan didaftarkan.
        Returns:
            bool: True jika registrasi sukses, False jika gagal."""
        logging.info(f"\n--- Memulai Proses Registrasi untuk NIM: {mhs.nim} ---")
        
        # Iterasi melalui daftar aturan (Delegasi tugas, memenuhi OCP dan DIP)
        for rule in self.validation_rules:
            if not rule.validate(mhs):
                logging.warning(f"REGISTRASI GAGAL! Dibatalkan oleh aturan {type(rule).__name__}.")
                return False
        
        logging.info(f"\nREGISTRASI SUKSES! Mahasiswa dengan NIM {mhs.nim} terdaftar.")
        return True

# 4. Challenge (Pembuktian OCP): Rule baru ditambahkan
class JadwalBentrokRule(IValidationRule):
    """Aturan validasi Jadwal Bentrok. Memperluas sistem tanpa mengubah RegistrationService (OCP)."""
    def validate(self, data: Mahasiswa) -> bool:
        """Simulasi logika pendeteksi bentrok jadwal."""
        if data.nim == '24111': # Simulasi bentrok jadwal untuk NIM Haris
            logging.warning("GAGAL : Terdeteksi bentrok jadwal mata kuliah.")
            return False
        logging.info("SUKSES : Tidak ada bentrok jadwal.")
        return True


# --- PROGRAM UTAMA & DEMONSTRASI ---

# 1. Setup Data Mahasiswa
Haris = Mahasiswa("24111", 26, True) # Gagal karena SKS (26) dan Jadwal Bentrok (NIM 24111)
Fikriadi = Mahasiswa("0244", 20, False) # Gagal karena Prasyarat (False)
Rafa = Mahasiswa("1049", 23, True) # Semua aturan sukses

# 2. Inisiasi Set Aturan LENGKAP, Termasuk Rule Challenge
daftar_aturan = [
    SksLimitRule(), 
    PrerequisiteRule(),
    JadwalBentrokRule() # <-- Rule baru, di inject (Pembuktian OCP)
]

# 3. Setup Layanan dengan Injection
reg_service = RegistrationService(validation_rules=daftar_aturan)

print("Perobaan 1: Gagal karena SKS terdeteksi bentrok")
reg_service.register_mhs(Haris) 

print("\nPerobaan 2: Gagal karena Prasyarat")
reg_service.register_mhs(Fikriadi)

print("\nPerobaan 3: Registrasi Sukses")
reg_service.register_mhs(Rafa)