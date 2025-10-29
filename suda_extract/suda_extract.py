import copy
from lxml import etree
import re
from yaml import safe_load
from yaml import safe_dump
from betacode_converter.betacode_converter import convert_betacode_to_unicode

htmlparser = etree.HTMLParser()


class ExtractEntry(object):

    def __init__(self, page_path: str) -> None:
        page_path = f'/home/ptrourke/workspace/github.com/ptrourke/sudareader/sol-entries/{page_path}'
        with open(page_path, 'r') as raw_page_handle:
            raw_page = raw_page_handle.read()
            root = etree.fromstring(raw_page, htmlparser)
            page_body = root.find('body')
            self.page_body = page_body

    def get_by_div_class_name(self, element_class_name: str) -> etree.Element:
        div_element = self.page_body.xpath(
            f'//div[@class="{element_class_name}"]'
        )[0]
        return div_element

    def get_strong_element_text(self, strong_text) -> str:
        vetting_status:str = ""
        strong_element = self.page_body.xpath(
            f'//strong[contains(text(), "{strong_text}")]'
        )[0]
        if strong_element.text:
            vetting_status = strong_element.text.replace(
                strong_text, ''
            ).strip()
        return vetting_status

    def get_text_between_strong_and_linebreak(self, strong_text: str) -> str:
        text_value: str = ''
        page_text = str(etree.tostring(self.page_body))
        subpattern = re.compile(
            f'<strong>{strong_text}[^<]*</strong>(.*?)<br ?/>'
        )
        text_value_match: re.Match = subpattern.search(page_text)
        if text_value_match:
            text_value_match_value: str = text_value_match.group(1)
            text_value += text_value_match_value
        return text_value


    def get_values_btw_strong_br(self, strong_text: str) -> etree.Element:
        element_name: str = re.sub(r'[^A-Za-z ]', '', strong_text)
        element_name = element_name.title()
        element_name = element_name.replace(' ', '')
        new_fragment: etree.Element = etree.Element(element_name)
        cursor_element: etree.Element = self.page_body.xpath(
            f'//strong[contains(text(), "{strong_text}")]'
        )[0]
        for next_element in cursor_element.itersiblings():
            if next_element.tag == 'br':
                break
            if next_element.tag == 'script':
                continue
            new_fragment.append(next_element)
        return new_fragment

    def convert_inline_greek(self, fragment: etree.Element) -> etree.Element:
        for child in fragment:
            if child.tag == 'g':
                greek_text = child.text
                greek_text = convert_betacode_to_unicode(greek_text)
                new_greek_text_element = etree.Element('em')
                new_greek_text_element.text = greek_text
                fragment.replace(child, new_greek_text_element)
        return fragment

    def get_adler_number(self) -> str:
        adler_fragment: etree.Element = self.get_values_btw_strong_br(
            "Adler number: "
        )
        adler_number_parts: list = adler_fragment.findall('span')
        adler_letter: str = adler_number_parts[0].text
        adler_item: str = adler_number_parts[1].text
        adler_number: str = f'{adler_letter},{adler_item}'
        return adler_number

    def get_headword(self) -> str:
        headword_fragment: etree.Element = self.get_values_btw_strong_br(
            "Headword:"
        )
        headword: str = headword_fragment.findtext('a')
        headword = convert_betacode_to_unicode(headword)
        return headword

    def get_translated_headword(self) -> str:
        translated_headword: str = self.get_text_between_strong_and_linebreak(
            "Translated headword:"
        )
        return translated_headword

    def get_translator(self) -> str:
        translator: etree.Element = self.get_values_btw_strong_br(
            'Translated by'
        )
        item: etree.Element
        translator_name: str = ''.join([etree.tostring(
            item
        ).decode('utf-8') for item in list(translator)])
        return str(translator_name)

    def get_translation(self) -> str:
        translation:etree.Element = self.get_by_div_class_name('translation')
        translation = self.convert_inline_greek(translation)
        translation_text: str = etree.tostring(translation).decode('utf-8')
        return str(translation_text)

    def get_notes(self):
        # TODO: Split notes by note number
        # TODO: Process links to cross-references
        # TODO: Processing links to Perseus
        notes = self.get_by_div_class_name('notes')
        notes = self.convert_inline_greek(notes)
        notes = etree.tostring(notes).decode('utf-8')
        return str(notes)

    def get_references(self) -> str:
        # TODO: Split notes by note number
        # TODO: Process links to cross-references
        # TODO: Processing links to Perseus
        references: etree.Element = self.get_by_div_class_name('bibliography')
        references = self.convert_inline_greek(references)
        reference_text: str = etree.tostring(references).decode('utf-8')
        return str(reference_text)

    def get_vetting_history(self) -> str:
        vetting_history: etree.Element = self.get_by_div_class_name('editor')
        vetting_history_text: str = etree.tostring(vetting_history).decode('utf-8')
        return str(vetting_history_text)

    def get_greek_original(self) -> str:
        greek_original_text: str = ''
        greek_original_element: etree.Element = self.get_by_div_class_name('greek')
        if not greek_original_element.text:
            return greek_original_text
        greek_original_text = greek_original_element.text
        greek_original_text = convert_betacode_to_unicode(greek_original_text)
        return greek_original_text

    def get_vetting_status(self) -> str:
        vetting_status: str = self.get_strong_element_text('Vetting Status: ')
        return vetting_status

    def get_from_strong_to_next_strong(
            self,
            strong_text: str,
            next_strong_text: str
    ) -> str:
        text_value: str = ''
        page_text: str = str(etree.tostring(self.page_body))
        subpattern = re.compile(
            f'<strong>{strong_text}[^<]*</strong>(.*?)<strong>{next_strong_text}'
        )
        text_match: re.Match = subpattern.search(page_text)
        if text_match:
            text_match_value: str = text_match.group(1)
            text_value += text_match_value
        return text_value

    def get_associated_internet_address(self) -> list:
        associated_add: str = self.get_from_strong_to_next_strong(
            'Associated internet address: ',
            'Keywords: '
        )
        assoc_add_text: etree.Element = etree.fromstring(
            associated_add,
            htmlparser
        )
        add_elem_list: etree.Element = assoc_add_text.find('body').findall('a')
        associated_addresses: list = []
        for add_elem in add_elem_list:
            href: str = add_elem.get('href')
            text: str = add_elem.text
            associated_addresses.append({'href': href, 'text': text})
        return associated_addresses

    def get_keywords(self) -> list:
        keywords: list = []
        keywords_raw: str = self.get_from_strong_to_next_strong(
            'Keywords: ',
            'Translated by'
        )
        if not keywords_raw:
            return keywords
        keyword_elements: etree.Element = etree.fromstring(
            keywords_raw,
            htmlparser
        )
        keyword_list: etree.Element = keyword_elements.find('body').findall('a')
        if not keyword_list:
            return keywords
        for keyword in keyword_list:
            if keyword.text:
                text: str = keyword.text
                keywords.append(text)
        return keywords

    def get_lemma_attributes(self) -> dict:
        lemma = {
            'associated_internet_addresses': self.get_associated_internet_address(),
            'adler_number': self.get_adler_number(),
            'headword': self.get_headword(),
            'translated_headword': self.get_translated_headword(),
            'vetting_status': self.get_vetting_status(),
            'vetting_history': self.get_vetting_history(),
            'greek_original': self.get_greek_original(),
            'translation': self.get_translation(),
            'notes': self.get_notes(),
            'references':self.get_references(),
            'keywords': self.get_keywords(),
            'translator': self.get_translator()
        }
        return lemma

lemma = ExtractEntry('rho/289')
print(safe_dump(lemma.get_lemma_attributes(), allow_unicode=True))




