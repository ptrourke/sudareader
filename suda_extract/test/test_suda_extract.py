import unittest

from lxml import etree

from settings import CODE_FILES
from suda_extract.suda_extract import ExtractEntry
htmlparser = etree.HTMLParser(encoding="utf-8")




class TestExtractEntry(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rho289 = ExtractEntry(f'{CODE_FILES}/suda_extract/test/test_files/rho289.html')

    def test_modify_sol_href(self):
        test_vectors = [
            {
                "test_value": "/~raphael/sol/sol-cgi-bin/search.cgi?db=REAL&field=adlerhw_gr&searchstr=alpha,1002",  # noqa E501
                "expected_result": "/lemma/alpha/1002/"
            }
        ]
        for test_vector in test_vectors:
            test_value = test_vector["test_value"]
            expected_result = test_vector["expected_result"]
            actual_result = ExtractEntry.modify_sol_href(test_value)
            self.assertEqual(expected_result, actual_result)

    def test_get_translator(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": '<a href="/credits/rho/289/">Andrea Consogno</a> on 12 November 2005@02:46:05.'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_translator()
            self.assertEqual(expected_result, actual_result)

    def test_get_translation(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result":
                '<div class="translation">A woodcarving tool.<br />\n"And an axe, and a bright plane, and a rounded drill."[1]<br />\nPlane [is] feminine.</div>\n'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_translation()
            self.assertEqual(expected_result, actual_result)
