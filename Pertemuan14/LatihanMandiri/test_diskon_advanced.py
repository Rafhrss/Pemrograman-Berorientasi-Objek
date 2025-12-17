import unittest
from diskon_service import DiskonCalculator

class TestDiskonLanjut(unittest.TestCase):

    def setUp(self):
        self.calc = DiskonCalculator()

    # Test 5 – Float Value
    def test_diskon_float_33_persen(self):
        """
        Diskon 33% dari 999:
        Harga setelah diskon = 669.33
        PPN 10% = 66.933
        Total = 736.263
        """
        hasil = self.calc.hitung_diskon(999, 33)
        self.assertAlmostEqual(hasil, 736.263, places=3)

    # Test 6 – Edge Case
    def test_harga_awal_nol(self):
        hasil = self.calc.hitung_diskon(0, 10)
        self.assertEqual(hasil, 0.0)

if __name__ == "__main__":
    unittest.main()