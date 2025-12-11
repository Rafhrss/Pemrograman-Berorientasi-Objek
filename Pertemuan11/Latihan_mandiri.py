# -------------------------------------------------
#  SEBELUM REFACTORING
# -------------------------------------------------

# class Mahasiswa:
#     def __init__(self, nim, sks_diambil, matkul_prasyarat=True):
#         self.nim = nim
#         self.sks_diambil = sks_diambil
#         self.matkul_prasyarat = matkul_prasyarat


# # === KODE BERMASALAH (SEBELUM REFACTORING) ===
# # Melanggar SRP, OCP, dan DIP
# class ValidatorManager:
#     SKS_LIMIT = 24

#     def __init__(self, data):
#         self.data = data # data adalah objek Mahasiswa

#     def validate_registration(self):
#         print(f"--- Memulai Validasi untuk NIM: {self.data.nim} ---")
        
#         if self.data.sks_diambil > self.SKS_LIMIT:
#             print(f"Gagal: Batas SKS terlampaui ({self.data.sks_diambil} > {self.SKS_LIMIT}).")
#             return False

#         if not self.data.matkul_prasyarat:
#             print("Gagal: Mata kuliah prasyarat belum dipenuhi.")
#             return False

#         print("Sukses: Registrasi valid.")
#         return True

# # Contoh Penggunaan Kode Bermasalah
# rafa = Mahasiswa("24111", 26, True)
# haris = Mahasiswa("1049", 20, False)

# manager_A = ValidatorManager(rafa)
# manager_B = ValidatorManager(haris)

# manager_A.validate_registration() # gagal karena SKS
# manager_B.validate_registration() # gagal karena Prasyarat






# -------------------------------------------------
#  SESUDAH REFACTORING
# -------------------------------------------------
from abc import ABC, abstractmethod

class Mahasiswa:
    def __init__(self, nim: str, sks_diambil: int, matkul_prasyarat: bool = True):
        self.nim = nim
        self.sks_diambil = sks_diambil
        self.matkul_prasyarat = matkul_prasyarat

# 2. Implementasi DIP/OCP: Abstraksi IValidationRule
class IValidationRule(ABC):
    """Abstraksi aturan validasi (Memenuhi DIP)"""
    @abstractmethod
    def validate(self, data: Mahasiswa) -> bool:
        pass

# 2. Implementasi DIP/OCP: Kelas Konkrit (Rules)
class SksLimitRule(IValidationRule):
    """Aturan validasi Batas SKS (Memenuhi SRP)."""
    SKS_LIMIT = 24

    def validate(self, data: Mahasiswa) -> bool:
        if data.sks_diambil > self.SKS_LIMIT:
            print(f"GAGAL : Batas SKS terlampaui ({data.sks_diambil} > {self.SKS_LIMIT}).")
            return False
        print("SUKSES : Batas SKS terpenuhi.")
        return True

class PrerequisiteRule(IValidationRule):
    """Aturan validasi Prasyarat Mata Kuliah (Memenuhi SRP)."""
    def validate(self, data: Mahasiswa) -> bool:
        if not data.matkul_prasyarat:
            print("GAGAL : Mata kuliah prasyarat belum dipenuhi.")
            return False
        print("SUKSES : Prasyarat terpenuhi.")
        return True

# 3. Implementasi SRP: Kelas Koordinator
class RegistrationService:
    """Tanggung jawab tunggal: Mengkoordinasi semua aturan validasi (SRP)."""
    def __init__(self, validation_rules: list[IValidationRule]):
        self.validation_rules = validation_rules

    def register_mhs(self, mhs: Mahasiswa) -> bool:
        print(f"\n--- Memulai Proses Registrasi untuk NIM: {mhs.nim} ---")
        # Iterasi melalui daftar aturan (Delegasi tugas, memenuhi OCP dan DIP)
        for rule in self.validation_rules:
            if not rule.validate(mhs):
                print(f"REGISTRASI GAGAL! Dibatalkan oleh aturan {type(rule).__name__}.")
                return False
        
        print(f"\nREGISTRASI SUKSES! Mahasiswa dengan NIM {mhs.nim} terdaftar.")
        return True

# 4. Challenge (Pembuktian OCP): Rule baru ditambahkan
class JadwalBentrokRule(IValidationRule):
    """Aturan validasi tanpa mengubah RegistrationService"""
    def validate(self, data: Mahasiswa) -> bool:
        if data.nim == '12345': # Simulasi bentrok jadwal untuk NIM tertentu
            print("GAGAL : Terdeteksi bentrok jadwal mata kuliah.")
            return False
        print("SUKSES : Tidak ada bentrok jadwal.")
        return True


# --- PROGRAM UTAMA & DEMONSTRASI ---

# 1. Setup Data Mahasiswa
Haris = Mahasiswa("24111", 26, True) # Gagal karena SKS & Bentrok
Fikriadi = Mahasiswa("0244", 20, False) # Gagal karena Prasyarat
Rafa = Mahasiswa("1049", 23, True) # Semua aturan sukses

# 2. Inisiasi Set Aturan LENGKAP, Termasuk Rule Challenge
daftar_aturan = [
    SksLimitRule(), 
    PrerequisiteRule(),
    JadwalBentrokRule() # ini Rule baru, di inject
]

# 3. Setup Layanan dengan Injection
reg_service = RegistrationService(validation_rules=daftar_aturan)

print("Perobaan 1: Gagal karena SKS terdeteksi bentrok")
reg_service.register_mhs(Haris) 

print("\nPerobaan 2: Gagal karena Prasyarat")
reg_service.register_mhs(Fikriadi)

print("\nPerobaan 3: Registrasi Sukses")
reg_service.register_mhs(Rafa)







