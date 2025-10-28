import re
import unicodedata

from betacode_converter.hash_code_mappings import hash_code_mappings


letters = {
    r"A": chr(0x03B1),  #  α alpha,
    r"B": chr(0x03B2),  # β beta,
    r"G": chr(0x00B3),  # γ gamma,
    r"D": chr(0x00B4),  # δ delta,
    r"E": chr(0x00B5),  # ε epsilon,
    r"Z": chr(0x00B6),  # ζ zeta,
    r"H": chr(0x00B7),  # η eta,
    r"Q": chr(0x00B8),  # "θ" theta,
    r"I": chr(0x00B9),  # "ι" iota,
    r"K": chr(0x00BA),  # "κ" kappa,
    r"L": chr(0x00BB),  # "λ" lambda,
    r"M": chr(0x00BC),  # "μ" mu,
    r"N": chr(0x00BD),  # "ν" nu,
    r"C": chr(0x00BE),  # "ξ" xi,
    r"O": chr(0x00BF),  # "ο" omicron,
    r"P": chr(0x00C0),  # "π" pi,
    r"R": chr(0x00C1),  # "ρ" rho,
    r"S": chr(0x00C2),  # "σ" sigma,
    r"T": chr(0x00C4),  # "τ" tau,
    r"U": chr(0x00C5),  # "υ" upsilon,
    r"F": chr(0x00C6),  # "φ" phi,
    r"X": chr(0x00C7),  # "χ" chi,
    r"Y": chr(0x00C8),  # "ψ" psi,
    r"W": chr(0x00C9),  # "ω" omega,
    r"V": chr(0x03DD),  # digamma

}

diacriticals = {
    r")": chr(0x0313),  # 'Smooth breathing',
    r"(": chr(0x0314),  # 'Rough breathing',
    r"/": chr(0x0301),  # 'Acute',
    r"\\": chr(0x0300),  # 'Grave',
    "=": chr(0x0342),  # 'Circumflex',
    "+": chr(0x308),  # 'diaresis'
    "|": chr(0x345),  # 'Iota subscript',
    "?": chr(0x323),  # 'Dot below',
}

punctuation = {
    r",": chr(0x002C),  # comma,
    r".": chr(0x002E),  # 'Period',
    r"'": chr(0x2019),  # 'Apostrophe',
    r":": chr(0x00B7),  # 'Colon',
    r";": chr(0x003B),  # 'Question Mark',
    r"-": chr(0x2010),  # 'Hyphen',
    r"_": chr(0x2014),  # 'Em-Dash',

}

white_space = {
    r" ": " ",  # 'Space',
}

mappings = {}
mappings.update(letters)
mappings.update(diacriticals)
mappings.update(punctuation)
mappings.update(white_space)


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
            if new_character not in diacriticals.values():
                new_character = new_character.upper()
                capitalize_next = False
        output_value.append(new_character)
    output_value = "".join(output_value)
    output_value = unicodedata.normalize("NFC", output_value)
    output_value = output_value.strip()
    return output_value
