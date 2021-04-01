import unittest
from main import filter_pdf_files


class TestSuite(unittest.TestCase):
    def test_filter_pdf_files(self):
        self.assertEqual([], filter_pdf_files(['', 'pdf', 'a.txt', 'main.py']))
        self.assertEqual(['a.pdf'], filter_pdf_files(['', 'pdf', 'a.pdf', 'main.py']))
