# -------------------------------------------------
#  SEBELUM REFACTORING
# -------------------------------------------------

# class Mahasiswa:
#     def __init__(self, nim, sks_diambil, telah_ambil_matkul_prasyarat=True):
#         self.nim = nim
#         self.sks_diambil = sks_diambil
#         self.telah_ambil_matkul_prasyarat = telah_ambil_matkul_prasyarat


# # === KODE BERMASALAH (SEBELUM REFACTORING) ===
# # Melanggar SRP, OCP, dan DIP
# class ValidatorManager:
#     SKS_LIMIT = 24

#     def __init__(self, data):
#         self.data = data # data adalah objek Mahasiswa

#     def validate_registration(self):
#         print(f"--- Memulai Validasi untuk NIM: {self.data.nim} ---")
        
#         if self.data.sks_diambil > self.SKS_LIMIT:
#             print(f"❌ Gagal: Batas SKS terlampaui ({self.data.sks_diambil} > {self.SKS_LIMIT}).")
#             return False

#         if not self.data.telah_ambil_matkul_prasyarat:
#             print("❌ Gagal: Mata kuliah prasyarat belum dipenuhi.")
#             return False

#         print("✅ Sukses: Registrasi valid.")
#         return True

# # Contoh Penggunaan Kode Bermasalah
# mahasiswa_A = Mahasiswa("12345", 26, True)
# mahasiswa_B = Mahasiswa("67890", 20, False)

# manager_A = ValidatorManager(mahasiswa_A)
# manager_B = ValidatorManager(mahasiswa_B)

# manager_A.validate_registration() # gagal karena SKS
# manager_B.validate_registration() # gagal karena Prasyarat






# -------------------------------------------------
#  SESUDAH REFACTORING
# -------------------------------------------------

# registration_service_solid.py
from abc import ABC, abstractmethod

class Mahasiswa:
    def __init__(self, nim: str, sks_diambil: int, telah_ambil_matkul_prasyarat: bool = True):
        self.nim = nim
        self.sks_diambil = sks_diambil
        self.telah_ambil_matkul_prasyarat = telah_ambil_matkul_prasyarat

# 2. Implementasi DIP/OCP: Abstraksi IValidationRule
class IValidationRule(ABC):
    """Abstraksi aturan validasi (Memenuhi DIP)"""
    @abstractmethod
    def validate(self, data: Mahasiswa) -> bool:
        pass

# 2. Implementasi DIP/OCP: Kelas Konkret (Rules)
class SksLimitRule(IValidationRule):
    """Aturan validasi Batas SKS (Memenuhi SRP)."""
    SKS_LIMIT = 24

    def validate(self, data: Mahasiswa) -> bool:
        if data.sks_diambil > self.SKS_LIMIT:
            print(f"❌ GAGAL (SKS): Batas SKS terlampaui ({data.sks_diambil} > {self.SKS_LIMIT}).")
            return False
        print("✅ SUKSES (SKS): Batas SKS terpenuhi.")
        return True

class PrerequisiteRule(IValidationRule):
    """Aturan validasi Prasyarat Mata Kuliah (Memenuhi SRP)."""
    def validate(self, data: Mahasiswa) -> bool:
        if not data.telah_ambil_matkul_prasyarat:
            print("❌ GAGAL (Prasyarat): Mata kuliah prasyarat belum dipenuhi.")
            return False
        print("✅ SUKSES (Prasyarat): Prasyarat terpenuhi.")
        return True

# 3. Implementasi SRP: Kelas Koordinator
class RegistrationService:
    """Tanggung jawab tunggal: Mengkoordinasi (menjalankan) semua aturan validasi (SRP)."""
    def __init__(self, validation_rules: list[IValidationRule]):
        self.validation_rules = validation_rules

    def register_student(self, student_data: Mahasiswa) -> bool:
        print(f"\n--- Memulai Proses Registrasi untuk NIM: {student_data.nim} ---")
        
        # Iterasi melalui daftar aturan (Delegasi tugas, memenuhi OCP dan DIP)
        for rule in self.validation_rules:
            if not rule.validate(student_data):
                print(f"🛑 REGISTRASI GAGAL! Dibatalkan oleh aturan {type(rule).__name__}.")
                return False
        
        print(f"\n🎉 REGISTRASI SUKSES! Mahasiswa {student_data.nim} terdaftar.")
        return True

# 4. Challenge (Pembuktian OCP): Rule baru ditambahkan
class JadwalBentrokRule(IValidationRule):
    """Aturan validasi tanpa mengubah RegistrationService"""
    def validate(self, data: Mahasiswa) -> bool:
        # Logika sederhana: Asumsikan Mahasiswa dengan NIM '12345' selalu bentrok
        if data.nim == '12345': 
            print("❌ GAGAL (Bentrok): Terdeteksi bentrok jadwal mata kuliah.")
            return False
        print("✅ SUKSES (Bentrok): Tidak ada bentrok jadwal.")
        return True

# --- PROGRAM UTAMA & DEMONSTRASI ---

# 1. Setup Data Mahasiswa
Haris = Mahasiswa("12345", 26, True) # Gagal karena SKS & Bentrok
Fikriadi = Mahasiswa("67890", 20, False) # Gagal karena Prasyarat
Rafa = Mahasiswa("00000", 20, True) # Semua aturan sukses

# 2. Inisiasi Set Aturan LENGKAP (Termasuk Rule Challenge)
full_rules = [
    SksLimitRule(), 
    PrerequisiteRule(),
    JadwalBentrokRule() # ini Rule baru, di inject
]

# 3. Setup Layanan dengan Injection
reg_service_challenge = RegistrationService(validation_rules=full_rules)

print("===== Skenario 1: Gagal karena SKS (dan terdeteksi bentrok) =====")
reg_service_challenge.register_student(Haris) 

print("\n===== Skenario 2: Gagal karena Prasyarat =====")
reg_service_challenge.register_student(Fikriadi)

print("\n===== Skenario 3: Registrasi Sukses =====")
reg_service_challenge.register_student(Rafa)







