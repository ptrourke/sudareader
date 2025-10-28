import re
import unicodedata

from betacode_converter.hash_code_mappings import hash_code_mappings

# Use chr() rather than character literals for precision.
greek_mappings = {
    r"A": chr(0x03B1),  # α alpha,
    r"B": chr(0x03B2),  # β beta,
    r"G": chr(0x03B3),  # γ gamma,
    r"D": chr(0x03B4),  # δ delta,
    r"E": chr(0x03B5),  # ε epsilon,
    r"Z": chr(0x03B6),  # ζ zeta,
    r"H": chr(0x03B7),  # η eta,
    r"Q": chr(0x03B8),  # θ theta,
    r"I": chr(0x03B9),  # ι iota,
    r"K": chr(0x03BA),  # κ kappa,
    r"L": chr(0x03BB),  # λ lambda,
    r"M": chr(0x03BC),  # μ mu,
    r"N": chr(0x03BD),  # ν nu,
    r"C": chr(0x03BE),  # ξ xi,
    r"O": chr(0x03BF),  # ο omicron,
    r"P": chr(0x03C0),  # π pi,
    r"R": chr(0x03C1),  # ρ rho,
    r"S": chr(0x03C2),  # σ sigma,
    r"T": chr(0x03C4),  # τ tau,
    r"U": chr(0x03C5),  # υ upsilon,
    r"F": chr(0x03C6),  # φ phi,
    r"X": chr(0x03C7),  # χ chi,
    r"Y": chr(0x03C8),  # ψ psi,
    r"W": chr(0x03C9),  # ω omega,
    r"V": chr(0x03DD),  # ϝ digamma
}

# The relevant Betacode values for diacriticals are
# converted to the Unicode values for the analogous combining
# diacritical, but then if the value for the parameter `normalize_nfc` is True
# (which is the default), the string is normalized to NFC pre-composed
# characters, otherwise the string is normalized to NFD combining characters.
combining_diacritical_mappings = {
    r")": chr(0x0313),  # ̓  'smooth breathing'
    r"(": chr(0x0314),  # ̔  'rough breathing'
    r"/": chr(0x0301),  #  ́ 'acute'
    r"\\": chr(0x0300),  #  ̀ 'grave'
    "=": chr(0x0342),  # ͂ 'circumflex',
    "+": chr(0x308),  #  ̈ 'diaresis'
    "|": chr(0x345),  # ͅ 'iota subscript',
    "?": chr(0x323),  #  ̣ 'dot below',
}

punctuation = {
    r",": chr(0x002C),  # , comma
    r".": chr(0x002E),  # . period
    r"'": chr(0x2019),  # ' apostrophe
    r":": chr(0x00B7),  # · colon
    r";": chr(0x003B),  # ; question mark
    r"-": chr(0x2010),  # ‐ hyphen
    r"_": chr(0x2014),  # — em-dash
}

white_space = {
    r" ": " ",  # " " space
    r"\n": "\n",  # line return
}

escape_codes_and_defaults = {
    '#': {'table': hash_code_mappings, 'default': chr(0x0374)},  # combining Greek number diacritical  noqa E501
}

mappings = {}
mappings.update(greek_mappings)
mappings.update(combining_diacritical_mappings)
mappings.update(punctuation)
mappings.update(white_space)

all_chars = list(mappings.keys()) + list(escape_codes_and_defaults.keys())
word_endings = list(punctuation.keys()) + list(white_space.keys())

def convert_betacode_to_unicode(
        string_value: str,
        normalize_nfc: bool = True
) -> str:
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
        if character_value not in all_chars:
            continue
        if character_value in "S":
            # look ahead
            if next_value == "1":  # medial sigma
                new_character = chr(0x03C3)
            elif next_value == "2":  # final sigma
                new_character = chr(0x03C2)
            elif next_value == "3":  # lunate sigma
                new_character = chr(0x03F2)
            elif next_value in word_endings:
                new_character = chr(0x03C2)  # final sigma
            else:
                new_character = chr(0x03C3)  # lunate sigma
        elif character_value in escape_codes_and_defaults.keys():
            if next_value not in "0123456789":
                new_character = escape_codes_and_defaults.get(
                    character_value
                ).get(
                    'default'
                )
            else:
                num_match = re.search(
                    r"[0123456789]+", string_value[index:]
                )
                if num_match:
                    special_char_number = num_match.group(0)
                    mapping_table = escape_codes_and_defaults.get(
                        character_value
                    ).get('table')
                    new_character = mapping_table.get(int(special_char_number))
        else:
            new_character = mappings.get(character_value)
        if capitalize_next:
            if new_character not in combining_diacritical_mappings.values():
                new_character = new_character.upper()
                capitalize_next = False
        output_value.append(new_character)
    output_value = "".join(output_value)
    if normalize_nfc:
        output_value = unicodedata.normalize("NFC", output_value)
    else:
        output_value = unicodedata.normalize("NFD", output_value)
    output_value = output_value.strip()
    return output_value
