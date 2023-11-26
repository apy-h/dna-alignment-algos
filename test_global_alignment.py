import unittest
from global_alignment import global_alignment

class TestGlobalAlignment(unittest.TestCase):
    def test_identical_sequences(self):
        self.assertEqual(global_alignment("ATCGT", "ATCGT"), ("ATCGT", "ATCGT"))

    def test_substring_sequences(self):
        self.assertEqual(global_alignment("ATCGT", "TCG"), ("ATCGT", "-TCG-"))

    def test_different_sequences(self):
        self.assertEqual(global_alignment("AAAAA", "TTTTT"), ("AAAAA", "TTTTT"))

    def test_empty_and_nonempty_sequences(self):
        self.assertEqual(global_alignment("", "ATCGT"), ("-----", "ATCGT"))

    def test_two_empty_sequences(self):
        self.assertEqual(global_alignment("", ""), ("", ""))

    def test_different_length_sequences(self):
        self.assertEqual(global_alignment("ATCGT", "AT"), ("ATCGT", "AT---"))

    def test_common_substring_sequences(self):
        self.assertEqual(global_alignment("ATCGT", "GTCGA"), ("ATCGT", "-GTCGA"))

if __name__ == '__main__':
    unittest.main()