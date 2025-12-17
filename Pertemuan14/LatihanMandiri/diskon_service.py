# ============ PROGRAM BUG BARU DENGAN PDB ==============

# import pdb

# class DiskonCalculator:
#     """Menghitung harga akhir setelah diskon."""

#     def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float:
#         pdb.set_trace()  # Debug point

#         # Hitung diskon
#         jumlah_diskon = harga_awal * persentase_diskon / 100
#         harga_setelah_diskon = harga_awal - jumlah_diskon

#         # BUG BARU: PPN 10% ditambahkan dua kali secara tidak sengaja
#         ppn = harga_setelah_diskon * 0.10
#         harga_akhir = harga_setelah_diskon + ppn
#         harga_akhir = harga_akhir + ppn  # <---- BUG: PPN ditambahkan dua kali

#         return harga_akhir




# ============ PROGRAM FINAL TANPA BUG DENGAN PDB  ==============

import pdb

class DiskonCalculator:
    """Menghitung harga akhir setelah diskon."""

    def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float:

        # Validasi boundary
        if harga_awal <= 0:
            return 0.0
        if persentase_diskon < 0:
            return harga_awal
        if persentase_diskon > 100:
            persentase_diskon = 100

        jumlah_diskon = harga_awal * persentase_diskon / 100
        harga_setelah_diskon = harga_awal - jumlah_diskon

        # PPN 10% (DITAMBAHKAN SEKALI SAJA)
        ppn = harga_setelah_diskon * 0.10
        harga_akhir = harga_setelah_diskon + ppn

        return harga_akhir