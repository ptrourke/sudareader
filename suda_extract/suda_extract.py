from lxml import etree
import re
from yaml import safe_dump
from betacode_converter.betacode_converter import convert_betacode_to_unicode

from settings import EXTRACT_SOURCE_FILES

htmlparser = etree.HTMLParser(encoding="utf-8")

class ExtractEntry(object):

    def __init__(self, page_path: str) -> None:
        with open(page_path, 'r') as raw_page_handle:
            raw_page: str = raw_page_handle.read()
            root: etree.Element = etree.fromstring(raw_page, htmlparser)
            page_body: etree.Element = root.find('body')
            page_body = self.convert_inline_greek(page_body)
            page_body = self.convert_suda_urls(page_body)
            self.page_body: etree.Element = page_body

    def extract_by_div_class_name(
            self,
            element_class_name: str
    ) -> etree.Element:
        div_element = self.page_body.xpath(
            f'//div[@class="{element_class_name}"]'
        )[0]
        return div_element

    def extract_strong_element_text(self, strong_text) -> str:
        vetting_status:str = ""
        strong_element = self.page_body.xpath(
            f'//strong[contains(text(), "{strong_text}")]'
        )[0]
        if strong_element.text:
            vetting_status = strong_element.text.replace(
                strong_text, ''
            ).strip()
        return vetting_status

    def extract_from_strong_to_next_strong(
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

    def extract_text_between_strong_and_linebreak(
            self,
            strong_text: str
    ) -> str:
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

    def extract_values_btw_strong_br(
        self,
        strong_text: str
    ) -> etree.Element:
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

    @staticmethod
    def modify_sol_href(href_value: str) -> str:
        if "~raphael" in href_value:
            href_value = href_value.replace("&amp;", "&")
            href_value = href_value.replace("%20", "+")
            href_value = href_value.replace("enlogin=guest&", "")
            href_value = href_value.replace("login=guest&", "")
            href_value = href_value.replace("db=REAL&", "")

            if href_value.startswith("/~raphael/sol/sol-cgi-bin/search.cgi?"):
                field_name_pattern = re.compile("field=([^&]+)")
                search_string_pattern = re.compile("searchstr=(.+)")
                field_name_match = field_name_pattern.search(href_value)
                search_string_match = search_string_pattern.search(href_value)
                if search_string_match:
                    search_string = search_string_match.group(1)
                else:
                    return "/search/"
                if field_name_match:
                    field_name = field_name_match.group(1)
                else:
                    return f"/search/{search_string}"
                if field_name == "adlerhw_gr":
                    search_string_parts = search_string.strip().split(',')
                    adler_letter = search_string_parts[0]
                    adler_number = search_string_parts[1]
                    href_value = f"/lemma/{adler_letter}/{adler_number}/"
                    return href_value
                href_value = f"/search/{field_name}/{search_string}"
                return href_value
            if href_value.startswith("/~raphael/sol/finder/showlinks.cgi?kws="):
                full_text_search = href_value.replace("/~raphael/sol/finder/showlinks.cgi?kws=", "")
                href_value = f"/search/{full_text_search}/"
                return href_value
            if href_value.startswith("/~raphael/sol/sol-html/icons/"):
                href_value = href_value.replace("/~raphael/sol/sol-html/icons/", "/images/")
                return href_value
            if href_value == "/~raphael/sol/sol-html/search.css":
                return "/style/search.css"
            if href_value.startswith("/~raphael/sol/sol-html"):
                href_value = href_value.replace("/~raphael/sol/sol-html", "/")
            if href_value.endswith("index.html"):
                href_value = href_value.replace("index.html", "")
        if href_value.startswith("http://"):
            href_value = href_value[7:]
            href_value = f"https://{href_value}"
        if href_value.startswith("mailto:suda@lsv.uky.edu"):
            href_value = href_value.replace("%20", "")
            subject_matter = href_value.split("?Subject")[-1]
            reference = subject_matter.split(",", 0)[-1]
            reference = reference.split(":")[-1]
            adler_letter, adler_number = reference.split(",")
            href_value = f"/credits/{adler_letter}/{adler_number}/"
        return href_value

    def convert_suda_urls(self, fragment: etree.Element) -> etree.Element:
        anchor_elements = fragment.xpath("//a")
        for element_item in anchor_elements:
            if element_item.tag == "a":
                href_value = element_item.get("href")
                href_value = self.modify_sol_href(href_value)
                element_item.attrib["href"] = href_value
        return fragment

    def convert_inline_greek(self, fragment: etree.Element) -> etree.Element:
        inline_greek_elements = fragment.xpath('//g')
        for element_item in inline_greek_elements:
            if element_item.tag == 'g':
                greek_text = element_item.text
                greek_text = convert_betacode_to_unicode(greek_text)
                new_greek_text_element = etree.Element('em')
                new_greek_text_element.text = greek_text
                parent_element = element_item.getparent()
                parent_element.replace(element_item, new_greek_text_element)
        return fragment

    def get_adler_reference(self) -> str:
        adler_fragment: etree.Element = self.extract_values_btw_strong_br(
            "Adler number: "
        )
        adler_number_parts: list = adler_fragment.findall('span')
        adler_letter: str = adler_number_parts[0].text
        adler_item: str = adler_number_parts[1].text
        adler_number: str = f'{adler_letter},{adler_item}'
        return adler_number

    def get_headword(self) -> str:
        headword_fragment: etree.Element = self.extract_values_btw_strong_br(
            "Headword:"
        )
        headword: str = headword_fragment.findtext('a')
        headword = convert_betacode_to_unicode(headword)
        return headword

    def get_translated_headword(self) -> str:
        translated_headword: str = self.extract_text_between_strong_and_linebreak(
            "Translated headword:"
        )
        return translated_headword

    def get_translator(self) -> str:
        translator: etree.Element = self.extract_values_btw_strong_br(
            'Translated by'
        )
        item: etree.Element
        translator_name: str = ''.join([etree.tostring(
            item
        ).decode('utf-8') for item in list(translator)])
        return str(translator_name)

    def get_translation(self) -> str:
        translation:etree.Element = self.extract_by_div_class_name('translation')
        translation_text: str = etree.tostring(translation).decode('utf-8')
        return str(translation_text)

    def get_notes(self):
        # TODO: Split notes by note number
        notes = self.extract_by_div_class_name('notes')
        notes = etree.tostring(notes).decode('utf-8')
        return str(notes)

    def get_references(self) -> str:
        # TODO: Split notes by note number
        references: etree.Element = self.extract_by_div_class_name('bibliography')
        reference_text: str = etree.tostring(references).decode('utf-8')
        return str(reference_text)

    def get_vetting_history(self) -> str:
        vetting_history: etree.Element = self.extract_by_div_class_name('editor')
        vetting_history_text: str = etree.tostring(vetting_history).decode('utf-8')
        return str(vetting_history_text)

    def get_greek_original(self) -> str:
        greek_original_text: str = ''
        greek_original_element: etree.Element = self.extract_by_div_class_name('greek')
        if not greek_original_element.text:
            return greek_original_text
        greek_original_text = greek_original_element.text
        greek_original_text = convert_betacode_to_unicode(greek_original_text)
        return greek_original_text

    def get_vetting_status(self) -> str:
        vetting_status: str = self.extract_strong_element_text('Vetting Status: ')
        return vetting_status

    def get_associated_internet_address(self) -> list:
        associated_add: str = self.extract_from_strong_to_next_strong(
            'Associated internet address: ',
            'Keywords: '
        )
        assoc_add_text: etree.Element = etree.fromstring(
            associated_add,
            htmlparser,

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
        keywords_raw: str = self.extract_from_strong_to_next_strong(
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
            'adler_reference': self.get_adler_reference(),
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

# lemma = ExtractEntry(f'{EXTRACT_SOURCE_FILES}/rho/289')
# print(safe_dump(lemma.get_lemma_attributes(), allow_unicode=True))




