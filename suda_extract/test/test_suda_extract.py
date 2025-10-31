import unittest

from suda_extract.suda_extract import ExtractEntry


class TestExtractEntry(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
