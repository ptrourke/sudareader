import unittest

from lxml import etree

from settings import CODE_FILES
from suda_extract.suda_extract import ExtractEntry
htmlparser = etree.HTMLParser(encoding="utf-8")


class TestExtractEntry(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rho289 = ExtractEntry(f'{CODE_FILES}/suda_extract/test/test_files/rho289.html')

    # def test_convert_suda_urls(self):
    #     TODO: implement test for convert_suda_urls
    #     raise Exception('Not implemented!')
    #
    # def test_convert_inline_greek(self):
    #     TODO: implement test for convert_inline_greek
    #     raise Exception('Not implemented!')

    def test_extract_element_by_div_class_name(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "test_value": "bibliography",
                "expected_result":
                    '<div class="bibliography">A.S.F. Gow and D.L. Page, eds., <i>The Greek Anthology: Hellenistic Epigrams</i>, vol. I, (Cambridge, 1965)<br />\nA.S.F. Gow and D.L. Page, eds., <i>The Greek Anthology: Hellenistic Epigrams</i>, vol. II, (Cambridge, 1965)<br />\nW.R. Paton, ed. <i>The Greek Anthology: Books I-VI</i>, (Cambridge, MA, 1999)</div>'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            test_value = test_vector["test_value"]
            expected_result = test_vector["expected_result"]
            actual_result_raw = test_file.extract_element_by_div_class_name(test_value)
            actual_result = etree.tostring(
                actual_result_raw
            ).decode('utf-8').strip()
            self.assertEqual(expected_result, actual_result)

    def test_extract_elements_between_strong_and_linebreak(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "test_value": "Adler number: ",
                "expected_result":
                    '<AdlerNumber><span class="target">rho</span>,<span class="target">289</span>\n</AdlerNumber>'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            test_value = test_vector["test_value"]
            expected_result = test_vector["expected_result"]
            actual_result_raw = test_file.extract_elements_between_strong_and_linebreak(test_value)
            actual_result = etree.tostring(
                actual_result_raw
            ).decode('utf-8').strip()
            self.assertEqual(expected_result, actual_result)

    def test_extract_text_between_strong_elements(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "test_values": ["Keywords: ", "Translated by"],
                "expected_result":
                    '<a href="/search/keyword/daily+life">daily life</a>; <a href="/search/keyword/definition">definition</a>; <a href="/search/keyword/dialects,+grammar,+and+etymology">dialects, grammar, and etymology</a>; <a href="/search/keyword/poetry">poetry</a>; <a href="/search/keyword/religion">religion</a>; <a href="/search/keyword/science+and+technology">science and technology</a>; <a href="/search/keyword/trade+and+manufacture">trade and manufacture</a><br />'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            test_values = test_vector["test_values"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.extract_text_between_strong_elements(
                test_values[0], test_values[1]
            )
            self.assertEqual(expected_result, actual_result)

    def test_extract_text_between_strong_and_linebreak(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "test_value": "Translated headword:",
                "expected_result": 'plane'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            test_value = test_vector["test_value"]
            expected_result = test_vector["expected_result"]
            actual_result =\
                test_file.extract_text_between_strong_and_linebreak(
                    test_value
                )
            self.assertEqual(expected_result, actual_result)

    def test_extract_text_from_strong_element(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "test_value": "Vetting Status: ",
                "expected_result": 'high'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            test_value = test_vector["test_value"]
            expected_result = test_vector["expected_result"]
            actual_result =\
                test_file.extract_text_from_strong_element(
                    test_value
                )
            self.assertEqual(expected_result, actual_result)

    def test_modify_inline_greek_text(self):
        test_vectors = [
            {
                "test_value": "<g>pepo/tai</g>",  # noqa E501
                "expected_result": "<em>&#960;&#949;&#960;&#972;&#964;&#945;&#953;</em>",  # noqa E501
                "preferred_result": "<em>πεπόηται</em>"
            }
        ]
        for test_vector in test_vectors:
            test_value = test_vector["test_value"]
            test_value = etree.fromstring(test_value)
            expected_result = test_vector["expected_result"]
            actual_result = ExtractEntry.modify_inline_greek_text(test_value)
            actual_result = etree.tostring(
                actual_result
            ).decode('utf-8').strip()
            self.assertEqual(expected_result, actual_result)

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

    def test_get_adler_reference(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": 'rho,289'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_adler_reference()
            self.assertEqual(expected_result, actual_result)

    def test_get_associated_internet_addresses(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": {
                    1: 'https://www.perseus.tufts.edu/hopper/text?'
                        'doc=Perseus:text:1999.04.0057:entry=eu)agh/s3',
                },
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_associated_internet_addresses()
            self.assertEqual(expected_result, actual_result)

    def test_get_greek_original(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": '̔Ρυκάνα· τεκτονικον ἐργαλεῖον. και πέλεκυν, ῥυκάναν τ’ εὐαγέα, και περιαγες τρύπανον. θηλυκῶς ἡ ῥυκάνα.'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_greek_original()
            self.assertEqual(expected_result, actual_result)

    def test_get_headword(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": '̔Ρυκάνα'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_headword()
            self.assertEqual(expected_result, actual_result)

    def test_get_keywords(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": [
                    'daily life',
                    'definition',
                    'dialects, grammar, and etymology',
                    'poetry',
                    'religion',
                    'science and technology',
                    'trade and manufacture'
                ]
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_keywords()
            self.assertEqual(expected_result, actual_result)

    def test_get_notes(self):
        self.maxDiff = None
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result":
                    '<div class="notes">[1] <span class="title">Greek Anthology</span> 6.204.3-4 (<a href="/search/Leonidas/">Leonidas</a> of <a href="https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0006:id=Tarentum">Tarentum</a>), a carpenter retiring from his trade dedicates tools to Athena; cf. Gow and Page (vol. I, 109), (vol. II, 316), and other extracts from this epigram at <a href="/lemma/delta/108/">delta 108</a> and <a href="/lemma/pi/2298/">pi 2298</a>. Gow and Page find (ibid.) the rendering of <em>&#949;&#8016;&#945;&#947;&#941;&#945;</em><i>bright</i>, <i>clear</i>, <i>conspicuous</i>; cf. LSJ s.v. (web address 1)) into English as <i>bright</i> (cf. Paton (404-405)) to be "plainly unsuitable". Although it is quite plausible that the sharpened blade of a wood plane would indeed be shiny and bright on its cutting edge, Gow and Page endorse (ibid.) such emendations as <em>&#949;&#8016;&#940;&#954;&#949;&#945;</em><em>&#949;&#8016;&#942;&#954;&#949;&#945;</em><i>sharp-edged</i>), <em>&#949;&#8016;&#960;&#945;&#947;&#941;&#945;</em><i>well-constructed</i>), and <em>&#949;&#8016;&#945;&#967;&#941;&#945;</em><i>well-sounding</i>).</div>\n'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_notes()
            self.assertEqual(expected_result, actual_result)

    def test_get_references(self):
        self.maxDiff = None
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": [
                    "A.S.F. Gow and D.L. Page, eds., <i>The Greek Anthology: Hellenistic Epigrams</i>, vol. I, (Cambridge, 1965)",
                    "A.S.F. Gow and D.L. Page, eds., <i>The Greek Anthology: Hellenistic Epigrams</i>, vol. II, (Cambridge, 1965)",
                    "W.R. Paton, ed. <i>The Greek Anthology: Books I-VI</i>, (Cambridge, MA, 1999)"
                ],
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_references()
            self.assertEqual(expected_result, actual_result)

    def test_get_translated_headword(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": 'plane'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_translated_headword()
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

    def test_get_vetting_history(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": [
                    {
                        "changed_by": "David Whitehead",
                        "change": "added note; modified keywords; cosmetics",
                        "change_date": "2005-11-13T04:55:38Z"
                    },
                    {
                        "changed_by": "David Whitehead",
                        "change": "",
                        "change_date": "2011-08-25T05:44:52Z"
                    },
                    {
                        "changed_by": "David Whitehead",
                        "change": "coding",
                        "change_date": "2016-05-25T07:38:33Z"
                    },
                    {
                        "changed_by": "Ronald Allen",
                        "change": "expanded n.1, added bibliography, added cross-references, added keyword",
                        "change_date":  "2021-02-16T18:28:34Z"
                    },
                ],
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_vetting_history()
            self.assertEqual(expected_result, actual_result)

    def test_get_vetting_status(self):
        test_vectors = [
            {
                "test_file": self.rho289,
                "expected_result": 'high'  # noqa E501
            }
        ]
        for test_vector in test_vectors:
            test_file = test_vector["test_file"]
            expected_result = test_vector["expected_result"]
            actual_result = test_file.get_vetting_status()
            self.assertEqual(expected_result, actual_result)
