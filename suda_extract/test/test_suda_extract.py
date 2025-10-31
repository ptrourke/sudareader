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
    #     raise Exception('Not implemented!')
    #
    # def test_convert_inline_greek(self):
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
                "expected_result": [
                    {
                        'href':
                            'https://www.perseus.tufts.edu/hopper/text?'
                            'doc=Perseus:text:1999.04.0057:entry=eu)agh/s3',
                        'text': 'Web address 1'
                    }
                ]  # noqa E501
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
                "expected_result":
                    '<div class="bibliography">A.S.F. Gow and D.L. Page, eds., <i>The Greek Anthology: Hellenistic Epigrams</i>, vol. I, (Cambridge, 1965)<br />\nA.S.F. Gow and D.L. Page, eds., <i>The Greek Anthology: Hellenistic Epigrams</i>, vol. II, (Cambridge, 1965)<br />\nW.R. Paton, ed. <i>The Greek Anthology: Books I-VI</i>, (Cambridge, MA, 1999)</div>\n'  # noqa E501
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
                "expected_result": '<div class="editor"><a href="/credits/rho/289/">David Whitehead</a> (added note; modified keywords; cosmetics) on 13 November 2005@04:55:38.<br />\n<a href="/credits/rho/289/">David Whitehead</a> on 25 August 2011@05:44:52.<br />\n<a href="/credits/rho/289/">David Whitehead</a> (coding) on 25 May 2016@07:38:33.<br />\n<a href="/credits/rho/289/">Ronald Allen</a> (expanded n.1, added bibliography, added cross-references, added keyword) on 16 February 2021@18:28:34.<br />\n</div>'  # noqa E501
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
