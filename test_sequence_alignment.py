from abc import ABC, abstractmethod
import unittest
from sequence_alignment import GlobalAlignment, LocalAlignment


class TestCase:
   def __init__(self, input_seq, expected_global_output, expected_local_output):
       self.input_seq = input_seq
       self.expected_global_output = expected_global_output
       self.expected_local_output = expected_local_output

#############################

class TestAlignment(ABC, unittest.TestCase):
   SAME_LENGTH_SEQ_CASES = [
       TestCase(("TGGTG", "ATCGT"), ("-TGGTG", "ATCGT-"), ("GT", "GT")),
       TestCase(("TCGTAGG", "CTCGTAT"), ("-TCGTAGG", "CTCGTAT-"), ("TCGTA", "TCGTA")),
       TestCase(("ATCGT", "GTCGA"), ("ATCGT", "GTCGA"), ("TCG", "TCG"))
   ]

   DIFF_LENGTH_SEQ_CASES = [
       TestCase(("ATCGT", "AT"), ("ATCGT", "AT---"), ("AT", "AT")),
       TestCase(("ATCGTATCGT", "CGA"), ("ATCGTATCGT", "--CG-A----"), ("CG", "CG")),
       TestCase(("ATCGT", "TCG"), ("ATCGT", "-TCG-"), ("TCG", "TCG")),
       TestCase(("ATCGTATCGT", "TCGATCG"), ("ATCGTATCGT", "-TCG-ATCG-"), ("TCGTATCG", "TCG-ATCG")),
       TestCase(("ATCGTATCGT", "ATCTTTCGTC"), ("ATCGTATCGT-", "ATCTT-TCGTC"), ("ATCGTATCGT", "ATCTT-TCGT")),
       TestCase(("ATCGACC", "GCATCTA"), ("--ATCGACC", "GCATCTA--"), ("ATC", "ATC")),
       TestCase(("ACCTAAGG", "GGCTCAATCA"), ("ACCT-AAGG-", "GGCTCAATCA"), ("CT", "CT"))
   ]

   EMPTY_SEQ_CASES = [
       TestCase(("", "ATCGT"), ("-----", "ATCGT"), ("", "")),
       TestCase(("", ""), ("", ""), ("", ""))
   ]


   def run_test_cases(self, test_cases, AlignmentClass):
       for case in test_cases:
           with self.subTest(case=case):
               expected_output = case.expected_global_output if AlignmentClass == GlobalAlignment else case.expected_local_output
               self.assertEqual(AlignmentClass(case.input_seq).align, expected_output)


   @abstractmethod
   def test_same_length_seq(self):
       pass


   @abstractmethod
   def test_diff_length_seq(self):
       pass


   @abstractmethod
   def test_empty_seq(self):
       pass

#############################

# python3 -m unittest -v test_sequence_alignment.TestGlobalAlignment
class TestGlobalAlignment(TestAlignment):
   AlignmentClass = GlobalAlignment

   def test_same_length_seq(self):
       super().run_test_cases(self.SAME_LENGTH_SEQ_CASES, self.AlignmentClass)


   def test_diff_length_seq(self):
       super().run_test_cases(self.DIFF_LENGTH_SEQ_CASES, self.AlignmentClass)


   def test_empty_seq(self):
       super().run_test_cases(self.EMPTY_SEQ_CASES, self.AlignmentClass)

#############################

# python3 -m unittest -v test_sequence_alignment.TestLocalAlignment
class TestLocalAlignment(TestAlignment):
   AlignmentClass = LocalAlignment

   def test_same_length_seq(self):
       super().run_test_cases(self.SAME_LENGTH_SEQ_CASES, self.AlignmentClass)


   def test_diff_length_seq(self):
       super().run_test_cases(self.DIFF_LENGTH_SEQ_CASES, self.AlignmentClass)


   def test_empty_seq(self):
       super().run_test_cases(self.EMPTY_SEQ_CASES, self.AlignmentClass)

#############################

if __name__ == '__main__':
   unittest.main()