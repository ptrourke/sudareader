import unittest
from betacode_converter import betacode_converter


class TestBetaCodeConverter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_convert_betacode_to_unicode(self):
        test_vectors = [
            {
                "test_value": "e)Mo/lon *samfis s3jac #867",
                "expected_result": "ἐμόλον Σαμφις ϲαξ 𐅆",
            },
            {
                "test_value": "*ma/gos",
                "expected_result": "Μάγος",
                "comment": "Headword mu 25: Magos",
            },
            {
                "test_value": r"*ma/gos: ma/gous e)ka/loun tou\\s yeudei=s fantasi/as peritiqe/ntas e(autoi=s. a)po\\ tou/tou de\ kai\ tou\s farmakou\\s ma/gous e)/legon. *sofoklh=s: u(fei\s ma/gon toio/nde mhxanorra/fon. ",  # noqa E501
                "expected_result": "Μάγος· μάγους ἐκάλουν τους ψευδεῖς φαντασίας περιτιθέντας ἑαυτοῖς. ἀπο τούτου δε και τους φαρμακους μάγους ἔλεγον. Σοφοκλῆς· ὑφεις μάγον τοιόνδε μηχανορράφον.",  # noqa E501
                "comment": "Definition mu 25: Magos",
            },
        ]
        for test_vector in test_vectors:
            test_value = test_vector["test_value"]
            expected_result = test_vector["expected_result"]
            actual_result = betacode_converter.convert_betacode_to_unicode(test_value)
            self.assertEqual(expected_result, actual_result)
