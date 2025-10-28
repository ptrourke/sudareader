import copy
from lxml import etree
import re
from yaml import safe_load
from yaml import safe_dump
from betacode_converter.betacode_converter import convert_betacode_to_unicode

htmlparser = etree.HTMLParser()


class ExtractEntry(object):

    def __init__(self, page_path):
        page_path = f'/home/ptrourke/workspace/github.com/ptrourke/sudareader/sol-entries/{page_path}'
        with open(page_path, 'r') as raw_page_handle:
            raw_page = raw_page_handle.read()
            root = etree.fromstring(raw_page, htmlparser)
            page_body = root.find('body')
            self.page_body = page_body

    def get_by_div_class_name(self, class_name):
        div_element = self.page_body.xpath(f'//div[@class="{class_name}"]')[0]
        return div_element

    def get_strong_element_text(self, strong_text):
        """Vetting Status: """
        strong_element = self.page_body.xpath(
            f'//strong[contains(text(), "{strong_text}")]'
        )[0]
        if strong_element.text:
            return strong_element.text.replace(strong_text, '').strip()

    def get_text_between_strong_and_linebreak(self, strong_text):
        new_fragment = ''
        page_text = str(etree.tostring(self.page_body))
        subpattern = re.compile(
            f'<strong>{strong_text}[^<]*</strong>(.*?)<br ?/>'
        )
        new_fragment_match = subpattern.search(page_text)
        if new_fragment_match:
            new_fragment_match_value = new_fragment_match.group(1)
            new_fragment += new_fragment_match_value
        return new_fragment


    def get_values_between_strong_and_linebreak(self, strong_text):
        element_name = re.sub(r'[^A-Za-z ]', '', strong_text)
        element_name = element_name.title()
        element_name = element_name.replace(' ', '')
        new_fragment = etree.Element(element_name)
        cursor_element = self.page_body.xpath(
            f'//strong[contains(text(), "{strong_text}")]'
        )[0]
        for next_element in cursor_element.itersiblings():
            if next_element.tag == 'br':
                break
            if next_element.tag == 'script':
                continue
            new_fragment.append(next_element)
        return new_fragment

    def get_adler_number(self):
        adler_fragment = self.get_values_between_strong_and_linebreak(
            "Adler number: "
        )
        adler_number_parts = adler_fragment.findall('span')
        adler_letter = adler_number_parts[0].text
        adler_item = adler_number_parts[1].text
        adler_number = f'{adler_letter},{adler_item}'
        return adler_number

    def get_headword(self):
        headword_fragment = self.get_values_between_strong_and_linebreak(
            "Headword:"
        )
        headword = headword_fragment.findtext('a')
        headword = convert_betacode_to_unicode(headword)
        return headword

    def get_translated_headword(self):
        translated_headword = self.get_text_between_strong_and_linebreak(
            "Translated headword:"
        )
        return translated_headword

    def get_translation(self):
        # TODO: Process Greek
        translation = self.get_by_div_class_name('translation')
        translation = etree.tostring(translation).decode('utf-8')
        return str(translation)

    def get_notes(self):
        # TODO: Split notes by note number
        # TODO: Process Greek
        # TODO: Process links to cross-references
        # TODO: Processing links to Perseus
        notes = self.get_by_div_class_name('notes')
        notes = etree.tostring(notes).decode('utf-8')
        return str(notes)

    def get_references(self):
        # TODO: Split notes by note number
        # TODO: Process Greek
        # TODO: Process links to cross-references
        # TODO: Processing links to Perseus
        references = self.get_by_div_class_name('bibliography')
        references = etree.tostring(references).decode('utf-8')
        return str(references)

    def get_vetting_history(self):
        vetting_history = self.get_by_div_class_name('editor')
        vetting_history = etree.tostring(vetting_history).decode('utf-8')
        return str(vetting_history)

    def get_greek_original(self):
        greek_original_element = self.get_by_div_class_name('greek')
        greek_original = greek_original_element.text
        greek_original = convert_betacode_to_unicode(greek_original)
        return greek_original

    def get_vetting_status(self):
        return self.get_strong_element_text('Vetting Status: ')

    def get_lemma_attributes(self):
        lemma = {
            'adler_number': self.get_adler_number(),
            'headword': self.get_headword(),
            'translated_headword': self.get_translated_headword(),
            'vetting_status': self.get_vetting_status(),
            'vetting_history': self.get_vetting_history(),
            'greek_original': self.get_greek_original(),
            'translation': self.get_translation(),
            'notes': self.get_notes(),
            'references':self.get_references(),
        }
        return lemma

lemma = ExtractEntry('rho/289')
print(safe_dump(lemma.get_lemma_attributes(), allow_unicode=True))




