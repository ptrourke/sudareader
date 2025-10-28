import re
import unicodedata

from betacode_converter.hash_code_mappings import hash_code_mappings

"""
"""

mappings = {
    r"A": "α",
    r"B": "β",
    r"G": "γ",
    r"D": "δ",
    r"E": "ε",
    r"Z": "ζ",
    r"H": "η",
    r"Q": "θ",
    r"I": "ι",
    r"K": "κ",
    r"L": "λ",
    r"M": "μ",
    r"N": "ν",
    r"C": "ξ",
    r"O": "ο",
    r"P": "π",
    r"R": "ρ",
    r"S": "σ",
    r"T": "τ",
    r"U": "υ",
    r"F": "φ",
    r"X": "χ",
    r"Y": "ψ",
    r"W": "ω",
    r"V": chr(0x03DD),  # Digamma
    r")": chr(0x0313),  # 'Smooth breathing',
    r"(": chr(0x0314),  # 'Rough breathing',
    r"/": chr(0x0301),  # 'Acute',
    r"\\": chr(0x0300),  # 'Grave',
    "=": chr(0x0342),  # 'Circumflex',
    "+": chr(0x308),  # 'diaresis'
    "|": chr(0x345),  # 'Iota subscript',
    "?": chr(0x323),  # 'Dot below',
    r",": chr(0x002C),  # comma,
    r".": chr(0x002E),  # 'Period',
    r",": chr(0x2019),  # 'Apostrophe',
    r":": chr(0x00B7),  # 'Colon',
    r";": chr(0x003B),  # 'Question Mark',
    r"-": chr(0x2010),  # 'Hyphen',
    r"_": chr(0x2014),  # 'Em-Dash',
    r" ": " ",  #'Space',
}

test_value = "e)Mo/lon *samfis s3jac #867"


def convert_betacode_to_unicode(string_value: str) -> str:
    output_value = []
    string_value = string_value.upper()
    capitalize_next = False
    for index, character_value in enumerate(string_value):
        new_character = ""
        if (index + 1) < len(string_value):
            next_value = string_value[index + 1]
        else:
            next_value = " "
        if character_value in "*":
            capitalize_next = True
            continue
        all_chars = list(mappings.keys()) + ["#"]
        if character_value not in all_chars:
            continue
        if character_value in "S":
            # look ahead
            if next_value == "1":  # medial sigma
                new_character = chr(0x03C3)
            elif next_value in "2.,:;-_ ":  # final sigma
                new_character = chr(0x03C2)
            elif next_value == "3":  # lunate sigma
                new_character = chr(0x03F2)
            else:
                new_character = chr(0x03C3)
        elif character_value in "#":
            if next_value not in "0123456789":
                new_character = chr(0x0374)
            else:
                num_match = re.search(r"[0123456789]+", string_value[index:])
                if num_match:
                    special_char_number = num_match.group(0)
                    new_character = hash_code_mappings.get(int(special_char_number))
        else:
            new_character = mappings.get(character_value)
        if capitalize_next:
            new_character = new_character.upper()
            capitalize_next = False
        output_value.append(new_character)
    output_value = "".join(output_value)
    output_value = unicodedata.normalize("NFC", output_value)
    output_value = output_value.strip()
    return output_value
