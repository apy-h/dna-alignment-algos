import unittest
from sequence_alignment import GlobalAlignment

class TestGlobalAlignment(unittest.TestCase):
    def test_same_length_sequences(self):
        self.assertEqual(GlobalAlignment("TGGTG", "ATCGT").align, ("-TGGTG", "ATCGT-"))
        self.assertEqual(GlobalAlignment("TCGTAGG", "CTCGTAT").align, ("-TCGTAGG", "CTCGTAT-"))

    def test_different_length_sequences(self):
        self.assertEqual(GlobalAlignment("ATCGT", "AT").align, ("ATCGT", "AT---"))
        self.assertEqual(GlobalAlignment("ATCGTATCGT", "CGA").align, ("ATCGTATCGT", "--CG-A----"))

    def test_substring_sequences(self):
        self.assertEqual(GlobalAlignment("ATCGT", "TCG").align, ("ATCGT", "-TCG-"))
        self.assertEqual(GlobalAlignment("ATCGTATCGT", "TCGATCG").align, ("ATCGTATCGT", "-TCG-ATCG-"))

    def test_common_substring_sequences(self):
        self.assertEqual(GlobalAlignment("ATCGT", "GTCGA").align, ("ATCGT", "GTCGA"))
        self.assertEqual(GlobalAlignment("ATCGTATCGT", "ATCTTTCGTC").align, ("ATCGTATCGT-", "ATCTT-TCGTC"))

    def test_different_sequences(self):
        self.assertEqual(GlobalAlignment("AAAAA", "TTTTT").align, ("AAAAA", "TTTTT"))
        self.assertEqual(GlobalAlignment("ATCGACC", "GCATCTA").align, ("--ATCGACC", "GCATCTA--"))

    def test_identical_sequences(self):
        self.assertEqual(GlobalAlignment("ATCGT", "ATCGT").align, ("ATCGT", "ATCGT"))
        self.assertEqual(GlobalAlignment("ATCGTATCGT", "ATCGTATCGT").align, ("ATCGTATCGT", "ATCGTATCGT"))

    def test_empty_and_nonempty_sequences(self):
        self.assertEqual(GlobalAlignment("", "ATCGT").align, ("-----", "ATCGT"))
        self.assertEqual(GlobalAlignment("", "ATCGTATCGT").align, ("----------", "ATCGTATCGT"))

    def test_two_empty_sequences(self):
        self.assertEqual(GlobalAlignment("", "").align, ("", ""))


if __name__ == '__main__':
    unittest.main()