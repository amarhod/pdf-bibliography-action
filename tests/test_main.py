import unittest
from main import filter_pdf_files, find_reference_list, prettify_reference


REF1 = {'linemarker': ['1'], 'raw_ref': ['[1] Michel Goossens, Frank Mittelbach, and Alexander Samarin. The L A TEX Companion. Addison-Wesley, Reading, Massachusetts, 1993.'],
        'misc': ['Michel Goossens, Frank Mittelbach, and Alexander Samarin', 'Reading, Massachusetts'],
        'author': ['The L A TEX Companion'], 'publisher': ['Addison-Wesley'], 'year': ['1993']}
REF2 = {'linemarker': ['2'], 'raw_ref': ['[2] Albert Einstein. Zur Elektrodynamik bewegter Körper. (German) [On the electrodynamics of moving bodies]. Annalen der Physik, 322(10):891–921, 1905.'],
        'misc': ['Albert Einstein. Zur Elektrodynamik bewegter Körper. (German) [On the electrodynamics of moving bodies]'],
        'journal_title': ['Ann. Phys. (Leipzig)'], 'journal_volume': ['322'], 'journal_year': ['1905'], 'journal_page': ['891-921'],
        'journal_reference': ['Ann. Phys. (Leipzig) 322 (1905) 891-921'], 'year': ['1905']}
REF3 = {'linemarker': ['3'], 'raw_ref': ['[3] Knuth: Computers and Typesetting, http://www-cs-faculty.stanford.edu/~uno/abcde.html 1'],
        'misc': ['Knuth: Computers and Typesetting', '1'], 'url': ['http://www-cs-faculty.stanford.edu/~uno/abcde.html']}


class TestSuite(unittest.TestCase):
    def test_filter_pdf_files(self):
        self.assertEqual([], filter_pdf_files(['', 'pdf', 'a.txt', 'main.py']))
        self.assertEqual(['a.pdf'], filter_pdf_files(['', 'pdf', 'a.pdf', 'main.py']))

    def test_find_reference_list(self):
        self.assertCountEqual([REF1, REF2, REF3], find_reference_list('examples/example_1.pdf'))

    def test_prettify_reference(self):
        self.assertEqual(REF1['raw_ref'][0], prettify_reference(REF1, verbosity=2))
        self.assertNotEqual(REF1['raw_ref'][0], prettify_reference(REF2, verbosity=2))
