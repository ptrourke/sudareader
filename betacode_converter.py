import unicodedata
import re

"""
"""

mappings = {
    r'A': 'α',
    r'B': 'β',
    r'G': 'γ',
    r'D': 'δ',
    r'E': 'ε',
    r'Z': 'ζ',
    r'H': 'η',
    r'Q': 'θ',
    r'I': 'ι',
    r'K': 'κ',
    r'L': 'λ',
    r'M': 'μ',
    r'N': 'ν',
    r'C': 'ξ',
    r'O': 'ο',
    r'P': 'π',
    r'R': 'ρ',
    r'S': 'σ',
    r'T': 'τ',
    r'U': 'υ',
    r'F': 'φ',
    r'X': 'χ',
    r'Y': 'ψ',
    r'W': 'ω',

    r'V': chr(0x03DD),  # Digamma
    r')': chr(0x0313),  # 'Smooth breathing',
    r'(': chr(0x0314),  # 'Rough breathing',
    r'/': chr(0x0301),  # 'Acute',
    r'\\': chr(0x0300),  # 'Grave',
    '=': chr(0x0342),  # 'Circumflex',
    '+': chr(0x308),  # 'diaresis'
    '|': chr(0x345),  # 'Iota subscript',
    '?': chr(0x323),  # 'Dot below',

    r'.': 'Period',
    r',': chr(0x2019),  # 'Apostrophe',
    r':': chr(0x00B7),  # 'Colon',
    r';': chr(0x003B),  # 'Question Mark',
    r'-': 'Hyphen',
    r'_': chr(0x2014),  # 'Em-Dash',
    r' ': ' ',  #'Space',
}

hash_mappings = {
    1: chr(0x03DF),  # ϟ Greek Letter Koppa
    2: chr(0x03DB),  # ϛ Greek Letter Stigma
    3: chr(0x03D9),  # ϙ Greek Letter Archaic Koppa
    4: chr(0x03DE),  # Ϛ Greek Letter Koppa Variant
    5: chr(0x03E1),  # ϡ Greek Letter Sampi
    6: chr(0x2E0F),  # ⸏ Paragraphos 31
    8: chr(0x2E10),  # ⸐ Forked Paragraphos
    9: chr(0x0301),  # ◌́ Combining Acute Accent
    10: chr(0x03FD),  # Ͻ Greek Capital Reversed Lunate
    11: chr(0x03FF),  # Ͽ Greek Capital Reversed Dotted
    12: chr(0x2014),  # — EM Dash
    13: chr(0x203B),  # ※ Reference Mark
    14: chr(0x2E16),  # ⸖ Dotted Right Pointing Angle
    15: chr(0x003E),  # > Greater-Than Sign
    16: chr(0x03FE),  # Ͼ Greek Capital Dotted Lunate Sigma
    17: chr(0x002F),  # / Solidus
    18: chr(0x003C),  # < Less-Than Sign
    19: chr(0x0300),  # ◌̀ Combining Grave Accent
    20: chr(0x10175),  # 𐅵 Greek One Half Sign
    21: chr(0x10176),  # 𐅶 Greek One Half Sign Alternate Form
    22: chr(0x0375),  # ͵ Greek Lower Numeral Sign
    23: chr(0x03D8),  # Ϙ Greek Letter Archaic Koppa
    24: chr(0x10176),  # 𐅶 Greek One Half Sign Alternate Form
    25: chr(0x10176),  # 𐅶 Greek One Half Sign Alternate Form
    26: chr(0x2E0F),  # ⸏ Paragraphos
    29: chr(0x00B7),  # · Middle Dot
    51: chr(0x00B7),  # · Middle Dot
    52: chr(0x205A),  # ⁚ Two Dot Punctuation
    53: chr(0x205D),  # ⁝ Tricolon
    55: chr(0x2059),  # ⁙ Five Dot Punctuation
    59: chr(0x03FD),  # Ͻ Greek Capital Reversed Lunate
    60: chr(0x0399),  # Ι Greek Capital Letter Iota
    61: chr(0x10142),  # 𐅂 Greek Acrophonic Attic One
    62: chr(0x10143),  # 𐅃 Greek Acrophonic Attic Five
    63: chr(0x0394),  # Δ Greek Capital Letter Delta
    64: chr(0x10144),  # 𐅄 Greek Acrophonic Attic Fifty
    65: chr(0x0397),  # Η Greek Capital Letter Eta
    66: chr(0x10145),  # 𐅅 Greek Acrophonic Attic Five
    67: chr(0x03A7),  # Χ
    68: chr(0x10146),  # 𐅆 Greek Acrophonic Attic Five
    69: chr(0x039C),  # Μ
    70: chr(0x002E),  # . Full Stop
    71: chr(0x00B7),  # · Middle Dot
    72: chr(0x02D9),  # ˙ Dot Above
    73: chr(0x205A),  # ⁚ Two Dot Punctuation
    74: chr(0x205D),  # ⁝ Tricolon
    75: chr(0x002E),  # . Full Stop
    80: chr(0x0308),  # ◌̈ Diaeresis
    81: chr(0x0027),  # ' Apostrophe
    82: chr(0x02CA),  # ˊ Modifier Acute Accent
    83: chr(0x02CB),  # ˋ Modifier Grave Accent
    84: chr(0x1FC0),  # ῀ Greek Perispomeni
    85: chr(0x02BD),  # ʽ Modifier Letter Reversed Comma 32
    86: chr(0x02BC),  # ʼ Modifier Letter Apostrophe 33
    90: chr(0x2014),  # — EM Dash
    100: chr(0x10186),  # 𐆆 Greek Artabe Sign
    101: chr(0x1017B),  # 𐅻 Greek Drachma Sign
    106: chr(0x10184),  # 𐆄 Greek Ounkia Sign
    112: chr(0x10188),  # 𐆈 Greek Gramma Sign
    113: chr(0x1017C),  # 𐅼 Greek Obol Sign
    114: chr(0x10140),  # 𐅀 Greek Acrophonic Attic One Quarter
    115: chr(0x10189),  # 𐆉 Greek Tryblion Base Sign
    116: chr(0x2053),  #  Swung Dash
    117: chr(0x10183),  # 𐆃 Greek Litra Symbol
    119: chr(0x1017D),  # ≈ Greek Two Obols Sign
    120: chr(0x10184),  # 𐆄 Greek Ounkia Sign
    122: chr(0x1017D),  # 𐅽 Greek Two Obols Sign
    123: chr(0x1017C),  # 𐅼 Greek Obol Sign
    128: chr(0x03FC),  # ϼ Greek Rho with Stroke Symbol
    130: chr(0x1018A),  # 𐆊 Greek Zero Sign
    131: chr(0x10177),  # 𐅷 Greek Two Thirds Sign
    135: chr(0x02D9),  # ˙ Dot Above
    136: chr(0x03A3),  # Σ Greek Capital Letter Sigma 35
    150: chr(0x221E),  # ∞ Infinity
    151: chr(0x2014),  # — EM Dash
    154: chr(0x2C80),  # Α Coptic Capital Letter Alfa
    156: chr(0x2310),  # ⌐ Reversed Not Sign
    161: chr(0x10175),  # 𐅵 Greek One Half Sign
    162: chr(0x25A1),  # □ White Square
    163: chr(0x0375),  # ͵ Greek Lower Numeral Sign
    166: chr(0x2A5A),  # ⩚ Logical And with Middle Stem
    169: chr(0x10175),  # 𐅵 Greek One Half Sign
    171: chr(0x10175),  # 𐅵 Greek One Half Sign
    172: chr(0x10176),  # 𐅶 Greek One Half Sign Alternate Form
    173: chr(0x10175),  # 𐅵 Greek One Half Sign
    200: chr(0x2643),  # ♃ Jupiter
    201: chr(0x25A1),  # □ White Square
    202: chr(0x264F),  # ♏ Scorpio
    203: chr(0x264D),  # ♍ Virgo
    204: chr(0x2640),  # ♀ Venus
    205: chr(0x2650),  # ♐ Sagittarius
    206: chr(0x2644),  # ♄ Saturn
    207: chr(0x2609),  #  Sun
    208: chr(0x263F),  # ☿ Mercury
    209: chr(0x263E),  # ☾ Last Quarter Moon
    210: chr(0x2642),  # ♂ Mars
    211: chr(0x2651),  # ♑ Capricorn
    212: chr(0x264C),  # ♌ Leo
    213: chr(0x2648),  # ♈ Aries
    214: chr(0x264E),  # ♎ Libra
    215: chr(0x264A),  # ♊ Gemini
    216: chr(0x264B),  # ♋ Cancer
    217: chr(0x2653),  # ♓ Pisces
    218: chr(0x2652),  # ♒ Aquarius
    219: chr(0x2649),  # ♉ Taurus
    220: chr(0x260D),  # ☍ Opposition
    221: chr(0x263D),  # ☽ First Quarter Moon
    222: chr(0x260C),  # ☌ Conjunction
    223: chr(0x2605),  #  Black Star
    240: chr(0x10177),  # 𐅷 Greek Two Thirds Sign
    241: chr(0x260B),  # ☋ Descending Node
    242: chr(0x2651),  # ♑ Capricorn
    244: chr(0x264C),  #  Leo
    303: chr(0x003E),  # > Diple Glyph Variant
    305: chr(0x2E0E),  # ⸎ Editorial Coronis
    310: chr(0x2E0E),  # ⸎ Editorial Coronis
    313: chr(0x2E0E),  # ⸎ Editorial Coronis
    315: chr(0x2E0E),  # ⸎ Editorial Coronis
    319: chr(0x25CF),  # ● Black Circle
    320: chr(0x2629),  # ☩ Cross of Jerusalem
    321: chr(0x2629),  # ☩ Cross of Jerusalem
    322: chr(0x2627),  # ☧ Chi-Rho
    323: chr(0x003E),  # > Greater-Than Sign
    451: chr(0x0283),  # ∫ Editorial Coronis Early Variant 37
    452: chr(0x2E10),  # ⸐ Forked Paragraphos
    453: chr(0x2E11),  # ⸑ Reverse Forked Paragraphos
    454: chr(0x2E10),  # ⸐ Forked Paragraphos
    455: chr(0x2E11),  # ⸑ Reverse Forked Paragraphos
    456: chr(0x2E0E),  # 󰈠 Editorial Coronis Early Variant 38
    458: chr(0x03A7),  # Χ Greek Capital Letter Chi
    459: chr(0x00B7),  # · Middle Dot
    460: chr(0x2014),  # — EM Dash
    461: chr(0x007C),  # | Vertical Line
    465: chr(0x2627),  # ☧ Chi-Rho
    467: chr(0x2192),  # → Rightwards Arrow
    468: chr(0x2E0E),  # Editorial Coronis Variant 39
    476: chr(0x0283),  # ∫ Small Letter Esh
    504: chr(0x2E0E),  # ⸎ Editorial Coronis
    505: chr(0x205C),  # ⁜ Dotted Cross Symbol
    506: chr(0x2E15),  # ⸕ Downward Ancora
    507: chr(0x2E14),  # ⸔ Upward Ancora
    508: chr(0x203B),  #  Reference Mark
    512: chr(0x03FD),  # Ͻ Greek Capital Reversed Lunate
    515: chr(0x10185),  # 𐆅 Greek Xestes Sign
    518: chr(0x10179),  # 𐅹 Greek Year sign
    519: chr(0x2191),  # ↑ Upward Arrow
    520: chr(0x2629),  # ☩ Cross of Jerusalem
    523: chr(0x2E13),  # ⸓ Dotted Obelus
    524: chr(0x2297),  # ⊗ Circled Times
    525: chr(0x271B),  #  Heavy Open Centre Cross
    526: chr(0x2190),  # ← Leftward arrow
    527: chr(0x02C6),  # ˆ Modifier Letter Circumflex Accent
    529: chr(0x204B),  # ⁋ Interpolation Marker
    531: chr(0x035C),  # ◌͜ Combining Double Breve Below
    532: chr(0x2E12),  # ⸒ Hypodiastole
    533: chr(0x03DA),  # 󰀺 Greek Capital Lunate Sigma Symbol
    544: chr(0x2058),  # ⁘ Four Dot Punctuation
    551: chr(0x25CC),  # ◌ Dotted circle
    556: chr(0x2629),  # ☩ Cross of Jerusalem
    561: chr(0x2191),  # ↑ Upward Arrow
    562: chr(0x0305),  # ◌̅ Combining Overline
    563: chr(0x1D242),  # ◌𝉂 Musical Triseme
    564: chr(0x1D243),  # ◌𝉃 Musical Tetraseme
    565: chr(0x1D244),  # ◌𝉄 Musical Pentaseme
    566: chr(0x1D231),  # 𝈱 Greek Instrumental Notation
    567: chr(0x1D213),  # 𝈓
    568: chr(0x1D233),  # 𝈳 Greek Instrumental Notation
    569: chr(0x1D236),  # 𝈶
    570: chr(0x03F9),  # Ϲ
    571: chr(0x10143),  # 𐅃 Greek Idiosyncratic Musical Symbol
    572: chr(0x1D229),  # 𝈩
    573: chr(0x1D212),  # 𝈒 Greek Vocal Notation Symbol-19
    574: chr(0x0393),  # Γ Greek Capital Letter Gamma
    575: chr(0x1D215),  # 𝈕 Greek Vocal Notation Symbol-22
    576: chr(0x1D216),  # 𝈖 Greek Vocal Notation Symbol-23
    577: chr(0x03A6),  # Φ Greek Capital Letter Phi
    578: chr(0x03A1),  # Ρ Greek Capital Letter Rho
    579: chr(0x039C),  # Μ Greek Capital Letter Mu
    580: chr(0x0399),  # Ι Greek Capital Letter Iota
    581: chr(0x0398),  # Θ Greek Capital Letter Theta
    582: chr(0x1D20D),  # 𝈍 Greek Vocal Notation Symbol-14
    583: chr(0x039D),  # Ν
    584: chr(0x2127),  # ℧ Inverted Ohm Sign
    585: chr(0x0396),  # Ζ
    586: chr(0x1D238),  # 𝈸 Greek Instrumental Notation
    587: chr(0x0395),  # Ε
    588: chr(0x1D208),  # 𝈈
    589: chr(0x1D21A),  # 𝈚 Greek Vocal Notation Symbol-52
    590: chr(0x1D23F),  # 𝈿 Greek Instrumental Notation
    591: chr(0x1D21B),  # 𝈛 Greek Vocal Notation Symbol-53
    592: chr(0x1D240),  # 𝉀 Greek Instrumental Notation
    593: chr(0x039B),  # Λ Greek Capital Letter Lambda
    598: chr(0x0394),  # Δ
    599: chr(0x1D214),  # 𝈔
    600: chr(0x1D228),  # 𝈨
    602: chr(0x1D237),  # 𝈷
    603: chr(0x03A0),  # Π Greek Capital Letter Pi
    604: chr(0x1D226),  # 𝈦
    615: chr(0x1D230),  # 𝈰
    616: chr(0x1D21E),  # 𝈞
    617: chr(0x03A9),  # Ω
    619: chr(0x03BB),  # λ Greek Small Letter Lambda
    621: chr(0x1D205),  # 𝈅
    622: chr(0x1D201),  # 𝈁 Greek Vocal Notation Symbol-2
    623: chr(0x2127),  # ℧
    624: chr(0x03FD),  # Ͻ
    627: chr(0x1D217),  # 𝈗 Greek Vocal Notation Symbol-24
    628: chr(0x039F),  # Ο Greek Capital Letter Omicron
    629: chr(0x039E),  # Ξ Greek Capital Letter Xi
    630: chr(0x0394),  # Δ
    631: chr(0x039A),  # Κ
    632: chr(0x1D20E),  # 𝈎 Greek Vocal Notation Symbol-15
    633: chr(0x1D232),  # 𝈲 Greek Instrumental Notation
    634: chr(0x1D239),  # 𝈹 Greek Instrumental Notation
    635: chr(0x1D200),  # 𝈀 Greek Vocal Notation Symbol-1
    636: chr(0x1D203),  # 𝈃 Greek Vocal Notation Symbol-4
    637: chr(0x1D206),  # 𝈆 Greek Vocal Notation Symbol-7
    638: chr(0x1D209),  # 𝈉 Greek Vocal Notation Symbol-10
    639: chr(0x1D20C),  # 𝈌 Greek Vocal Notation Symbol-13
    640: chr(0x1D211),  # 𝈑 Greek Vocal Notation Symbol-18
    641: chr(0x03A9),  # Ω Greek Capital Letter Omega
    642: chr(0x0397),  # Η
    643: chr(0x1D21D),  # 𝈝 Greek Instrumental Notation
    644: chr(0x1D21F),  # 𝈟 Greek Instrumental Notation
    645: chr(0x1D221),  # 𝈡 Greek Instrumental Notation
    646: chr(0x1D225),  # 𝈥 Greek Instrumental Notation
    647: chr(0x1D22C),  # 𝈬 Greek Instrumental Notation
    648: chr(0x1D235),  # 𝈵 Greek Instrumental Notation
    649: chr(0x1D20B),  # 𝈋 Greek Vocal Notation Symbol-12
    650: chr(0x1D20F),  # 𝈏 Greek Instrumental Notation
    651: chr(0x03A7),  # Χ Greek Capital Letter Chi
    652: chr(0x03A4),  # Τ Greek Capital Letter Tau
    653: chr(0x1D219),  # 𝈙 Greek Vocal Notation Symbol-51
    654: chr(0x1D21C),  # 𝈜 Greek Vocal Notation Symbol-54
    655: chr(0x1D202),  # 𝈂
    656: chr(0x1D224),  # 𝈤 Greek Instrumental Notation
    657: chr(0x1D22E),  # 𝈮 Greek Instrumental Notation
    658: chr(0x1D23E),  # 𝈾 Greek Instrumental Notation
    659: chr(0x1D241),  # 𝉁 Greek Instrumental Notation
    660: chr(0x0391),  # Α Greek Capital Letter Alpha
    661: chr(0x0392),  # Β Greek Capital Letter Beta
    662: chr(0x03A5),  # Υ Greek Capital Letter Upsilon
    663: chr(0x03A8),  # Ψ Greek Capital Letter Psi
    664: chr(0x1D23A),  # 𝈺 Greek Instrumental Notation
    665: chr(0x1D234),  # 𝈴 Greek Instrumental Notation
    666: chr(0x1D22F),  # 𝈯 Greek Instrumental Notation
    667: chr(0x1D22D),  # 𝈭 Greek Instrumental Notation
    668: chr(0x1D210),  # 𝈐 Greek Vocal Notation Symbol-17
    669: chr(0x1D20A),  # 𝈊 Greek Vocal Notation Symbol-11
    670: chr(0x1D207),  # 𝈇 Greek Vocal Notation Symbol-8
    671: chr(0x1D21B),  # 𝈛 Greek Vocal Notation Symbol-53
    672: chr(0x1D218),  # 𝈘 Greek Vocal Notation Symbol-50
    673: chr(0x1D223),  # 𝈣 Greek Instrumental Notation
    674: chr(0x1D222),  # 𝈢 Greek Instrumental Notation
    675: chr(0x1D240),  # 𝉀 Greek Instrumental Notation
    676: chr(0x1D23D),  # 𝈽 Greek Instrumental Notation
    677: chr(0x03BC),  # µ
    678: chr(0x1D220),  # 𝈠 Greek Instrumental Notation
    679: chr(0x1D204),  # 𝈄 Greek Vocal Notation Symbol-5
    683: chr(0x2733),  # ✳ Eight Spoked Asterisk
    684: chr(0x1D22A),  # 𝈪 Greek Instrumental Notation
    689: chr(0x10175),  # 𐅵 Greek One Half Sign
    690: chr(0x27D8),  # ⊥ Perpendicular Line Illustration
    691: chr(0x27C0),  # ⟀ Three-Dimensional Angle Illustration
    692: chr(0x27C1),  # ⟁ Contained Shape Illustration
    694: chr(0x1D23C),  # 𝈼 Instrumental Notation Symbol 49
    695: chr(0x2014),  # — Vocal Notation Symbol 16
    696: chr(0x1D227),  # 𝈧 Instrumental Notation Symbol 17
    697: chr(0x1D245),  # 𝉅 Greek Musical Lemma
    700: chr(0x205E),  # ⁞ Vertical Four Dots
    709: chr(0x223B),  #  Homothetic
    717: chr(0x2E00),  # ⸀ Right Angle Substitution Marker
    718: chr(0x2E01),  # ⸁ Right Angle Dotted Substitution
    719: chr(0x2E06),  # ⸆ Raised Interpolation Marker
    720: chr(0x2E07),  # ⸇ Raised Dotted Interpolation Marker
    722: chr(0x2135),  # ℵ Alef Symbol
    723: chr(0x1D516),  # 𝔖 Septuagint Reference
    724: chr(0x210C),  # ℌ Hebrew Old Testament
    725: chr(0x1D510),  # 𝔐 Majority Reading of New Testament
    730: chr(0x2014),  # — EM Dash
    731: chr(0x23D7),  # ⏗ Metrical Triseme
    732: chr(0x23D8),  # ⏘ Metrical Tetraseme
    733: chr(0x23D9),  # ⏙ Metrical Pentaseme
    751: chr(0x0661),  # ١ Arabic-Indic Digit One
    752: chr(0x0662),  # ٢ Arabic-Indic Digit Two
    753: chr(0x0663),  # ٣ Arabic-Indic Digit Three
    754: chr(0x0664),  # ٤ Arabic-Indic Digit Four
    755: chr(0x0665),  # ٥ Arabic-Indic Digit Five
    756: chr(0x0666),  # ٦ Arabic-Indic Digit Six
    757: chr(0x0667),  # ٧۷ Arabic-Indic Digit Seven
    758: chr(0x0668),  # ٨۸ Arabic-Indic Digit Eight
    759: chr(0x0669),  # ٩۹ Arabic-Indic Digit Nine
    760: chr(0x0660),  # ٠۰ Arabic-Indic Digit Zero
    762: chr(0x02D9),  # ˙ Dot Above
    800: chr(0x2733),  # ✳ Denarius 41 Definition: TLG has no information on this character
    801: chr(0x10141),  # 𐅁
    802: chr(0x10140),  # 𐅀 Greek Acrophonic Attic One Quarter
    803: chr(0x03A7),  # X
    804: chr(0x002F),  # /
    805: chr(0x03A4),  # T Greek Capital Letter Tau
    806: chr(0x039A),  # Κ Greek Capital Letter Kappa
    807: chr(0x10166),  # 𐅦 Greek Acrophonic Troezenian Fifty
    808: chr(0x10148),  # 𐅈 Greek Acrophonic Attic Five Talents
    811: chr(0x03A4),  # T Greek Capital Letter Tau
    812: chr(0x10148),  # 𐅈 Greek Acrophonic Attic Five Talents
    813: chr(0x10149),  # 𐅉 Greek Acrophonic Attic Ten Talents
    814: chr(0x1014A),  # 𐅊 Greek Acrophonic Attic Fifty Talents
    815: chr(0x1014B),  # 𐅋 Greek Acrophonic Attic One
    816: chr(0x1014C),  # 𐅌 Greek Acrophonic Attic Five
    817: chr(0x1014D),  # 𐅍 Greek Acrophonic Attic One
    818: chr(0x1014E),  # 𐅎 Greek Acrophonic Attic Five
    821: chr(0x03A3),  # Σ
    822: chr(0x1014F),  # 𐅏 Greek Acrophonic Troezenian Five
    823: chr(0x10150),  # 𐅐 Greek Acrophonic Attic Ten Staters
    824: chr(0x10151),  # 𐅑 Greek Acrophonic Attic Fifty Staters
    825: chr(0x10152),  # 𐅒 Greek Acrophonic Attic One
    826: chr(0x10153),  # 𐅓 Greek Acrophonic Attic Five
    827: chr(0x10154),  # 𐅔 Greek Acrophonic Attic One
    829: chr(0x10155),  # 𐅕 Greek Acrophonic Attic Ten
    830: chr(0x10147),  # 𐅇
    831: chr(0x10147),  # 𐅇
    832: chr(0x10156),  # 𐅖 Greek Acrophonic Attic Fifty
    833: chr(0x039C),  # Μ
    834: chr(0x10157),  # 𐅗 Greek Acrophonic Attic One Mnas
    835: chr(0x03A7),  # Χ Greek Capital Letter Xi
    836: chr(0x03A3),  # Σ
    837: chr(0x03A4),  # Τ Greek Capital Letter Tau
    838: chr(0x10143),  # 𐅃
    839: chr(0x10141),  # 𐅁
    842: chr(0x00B7),  # · Middle Dot
    843: chr(0x1015B),  # 𐅛 Greek Acrophonic Epidaurean Two
    844: chr(0x205D),  # ⁝ Tricolon
    845: chr(0x10158),  # 𐅘
    846: chr(0x10110),  # 𐄐 Aegean Number Ten
    847: chr(0x1015E),  # 𐅞
    848: chr(0x10112),  # 𐄒 Aegean Number Thirty
    853: chr(0x0399),  # Ι Greek Capital Letter Iota
    862: chr(0x0394),  # Δ Greek Capital Letter Delta
    863: chr(0x10144),  # 𐅄 ‣ Greek Acrophonic Attic Fifty
    865: chr(0x10145),  # 𐅅 ‣ Greek Acrophonic Attic Five
    866: chr(0x03A7),  # Χ
    867: chr(0x10146),  # 𐅆 Greek Acrophonic Attic Five
    922: chr(0x1D228),  # 𝈨
    925: chr(0x1D217),  # 𝈗 Greek Vocal Notation Symbol-24
    926: chr(0x1D232),  # 𝈲
    927: chr(0x0057),  # W Latin Capital Letter W
    928: chr(0x1D20B),  # 𝈋 Greek Vocal Notation Symbol-12
    929: chr(0x1D214),  # 𝈔 Greek Vocal Notation Symbol-21
    932: chr(0x2733),  # ✳ Eight Spoked Asterisk
    938: chr(0x01A7),  # Ƨ Latin Capital Letter Tone Two
    939: chr(0x007E),  # ~ Tilde
    941: chr(0x1D205),  # 𝈅 Illustration
    1000: chr(0x1017C),  # 𐅼 Greek Obol Sign
    1001: chr(0x1017D),  # 𐅽 Greek Two Obols Sign
    1002: chr(0x1017E),  # 𐅾 Greek Three Obols Sign
    1003: chr(0x1017F),  # 𐅾 Greek Four Obols Sign
    1004: chr(0x10180),  # 𐆀 Greek Five Obols Sign
    1005: chr(0x03A7),  # Χ Greek Capital Letter Chi
    1020: chr(0x003C),  # < Less-Than Sign
    1100: chr(0x2183),  # Ↄ Roman Numeral Reversed One
    1109: chr(0x003D),  # = Equals Sign
    1110: chr(0x002D),  # - Hyphen-Minus
    1111: chr(0x00B0),  # º Degree Sign
    1114: chr(0x1D201),  # 𝈁 Greek Vocal Notation Symbol-2
    1115: chr(0x007C),  # | Vertical Line
    1116: chr(0x01A7),  # Ƨ Latin Capital Letter Tone Two
    1117: chr(0x005A),  # Z Latin Capital letter Z
    1119: chr(0x0110),  # Đ Latin Capital Letter D with Stroke
    1121: chr(0x005A),  # Z Latin Capital letter Z
    1124: chr(0x211E),  #  Prescription Take
    1126: chr(0x004F),  # O Latin Capital Letter O
    1130: chr(0x005C),  # \ Reverse Solidus
    1135: chr(0x0039),  # 9 Digit Nine
    1136: chr(0x2112),  # ℒ Script Capital L
    1200: chr(0x00A2),  # ¢ Cent Sign
    1201: chr(0x2021),  # ‡ Double Dagger
    1202: chr(0x20A4),  # ₤ Pound Sign
    1203: chr(0x00DF),  # ß Latin Small Letter Sharp S
    1204: chr(0x00B0),  # º Degree Sign
    1209: chr(0x0127),  # ħ Latin Small Letter H with Stroke
    1213: chr(0x0152),  # Œ Latin Capital Ligature OE
    1214: chr(0x0153),  # œ Latin Small Ligature OE
    1215: chr(0x00C6),  # Æ Latin Capital Letter AE
    1216: chr(0x00E6),  # æ Latin Small Letter AE
    1219: chr(0x0024),  # $ Dollar Sign
    1220: chr(0x0040),  # @ Commercial At
    1221: chr(0x0131),  # ı Latin Small Letter Dotless I
    1222: chr(0x0130),  # İ Latin Capital Letter I with Dot
    1224: chr(0x2295),  # ⊕ Circled Plus
    1225: chr(0x00A9),  # © Copyright Sign
    1226: chr(0x2731),  #  Heavy Asterisk
    1227: chr(0x2021),  # ‡ Double Dagger
    1230: chr(0x25AD),  # ▭ White Rectangle
    1313: chr(0x223D),  # ∽ Reversed Tilde
    1316: chr(0x0292),  # ʒ Lowercase Ezh
    1318: chr(0x223B),  #  Homothetic
    1322: chr(0x2644),  #  Saturn
    1337: chr(0x003E),  # > Greater-Than Sign
    1338: chr(0x1017E),  # 𐅾 Greek Three Obols Sign
    1512: chr(0x003C),  # < Less-Than Sign
    1513: chr(0x10175),  # 𐅵 Greek One Half Sign
    1514: chr(0x00F7),  # ÷ Division Sign
    1515: chr(0x1D20F),  # 𝈏 Greek Vocal Notation Symbol-16
    1518: chr(0x1D229),  # 𝈩
    1521: chr(0x0222),  # Ȣ Latin Capital Letter OU
    1523: chr(0x205B),  # ⁛ Four Dot Mark
    1529: chr(0x2227),  # Upward Pointing Arrow
    1530: chr(0x2228),  # Downward Pointing Arrow
    1531: chr(0x03CF),  # ϗ Greek Capital Kai Symbol Definition: uppercase καί abbreviation
    1532: chr(0x03D7),  # ϗ Greek Kai Symbol Definition: lowercase καί abbreviation
    2000: chr(0x1D000),  # 𝀀 Byzantine Musical Symbol Psili
    2001: chr(0x1D001),  # 𝀁 Byzantine Musical Symbol Daseia
    2002: chr(0x1D002),  # 𝀂 Byzantine Musical Symbol
    2003: chr(0x1D003),  # 𝀃 Byzantine Musical Symbol Oxeia
    2004: chr(0x1D004),  # 𝀄 Byzantine Musical Symbol Oxeia
    2005: chr(0x1D005),  # 𝀅 Byzantine Musical Symbol Vareia
    2006: chr(0x1D006),  # 𝀆 Byzantine Musical Symbol Vareia
    2007: chr(0x1D007),  # 𝀇 Byzantine Musical Symbol Kathisti
    2008: chr(0x1D008),  # 𝀈 Byzantine Musical Symbol Syrmatiki
    2009: chr(0x1D009),  # 𝀉 Byzantine Musical Symbol Paraklitiki
    2010: chr(0x1D00A),  # 𝀊 Byzantine Musical Symbol Ypokrisis
    2011: chr(0x1D00B),  # 𝀋 Byzantine Musical Symbol Ypokrisis
    2012: chr(0x1D00C),  # 𝀌 Byzantine Musical Symbol Kremasti
    2013: chr(0x1D00D),  # 𝀍 Byzantine Musical Symbol Apeso
    2014: chr(0x1D00E),  # 𝀎 Byzantine Musical Symbol Exo
    2015: chr(0x1D00F),  # 𝀏 Byzantine Musical Symbol Teleia
    2016: chr(0x1D010),  # 𝀐 Byzantine Musical Symbol
    2017: chr(0x1D011),  # 𝀑 Byzantine Musical Symbol
    2018: chr(0x1D012),  # 𝀒 Byzantine Musical Symbol
    2019: chr(0x1D013),  # 𝀓 Byzantine Musical Symbol Synevma
    2020: chr(0x1D014),  # 𝀔 Byzantine Musical Symbol Thita
    2021: chr(0x1D015),  # 𝀕 Byzantine Musical Symbol Oligon
    2022: chr(0x1D016),  # 𝀖 Byzantine Musical Symbol Gorgon
    2023: chr(0x1D017),  # 𝀗 Byzantine Musical Symbol Psilon
    2024: chr(0x1D018),  # 𝀘 Byzantine Musical Symbol Chamilon
    2025: chr(0x1D019),  # 𝀙 Byzantine Musical Symbol Vathy
    2026: chr(0x1D01A),  # 𝀚 Byzantine Musical Symbol Ison
    2027: chr(0x1D01B),  # 𝀛 Byzantine Musical Symbol Kentima
    2028: chr(0x1D01C),  # 𝀜 Byzantine Musical Symbol
    2029: chr(0x1D01D),  # 𝀝 Byzantine Musical Symbol Saximata
    2030: chr(0x1D01E),  # 𝀞 Byzantine Musical Symbol Parichon
    2031: chr(0x1D01F),  # 𝀟 Byzantine Musical Symbol Stavros
    2032: chr(0x1D020),  # 𝀠 Byzantine Musical Symbol Oxeiai
    2033: chr(0x1D021),  # 𝀡 Byzantine Musical Symbol Vareiai
    2034: chr(0x1D022),  # 𝀢 Byzantine Musical Symbol
    2035: chr(0x1D023),  # 𝀣 Byzantine Musical Symbol
    2036: chr(0x1D024),  # 𝀤 Byzantine Musical Symbol Klasma
    2037: chr(0x1D025),  # 𝀥 Byzantine Musical Symbol Revma
    2038: chr(0x1D026),  # 𝀦 Byzantine Musical Symbol Piasma
    2039: chr(0x1D027),  # 𝀧 Byzantine Musical Symbol Tinagma
    2040: chr(0x1D028),  # 𝀨 Byzantine Musical Symbol
    2041: chr(0x1D029),  # 𝀩 Byzantine Musical Symbol Seisma
    2042: chr(0x1D02A),  # 𝀪 Byzantine Musical Symbol Synagma
    2043: chr(0x1D02B),  # 𝀫 Byzantine Musical Symbol Synagma
    2044: chr(0x1D02C),  # 𝀬 Byzantine Musical Symbol
    2045: chr(0x1D02D),  # 𝀭 Byzantine Musical Symbol Thema
    2046: chr(0x1D02E),  # 𝀮 Byzantine Musical Symbol Lemoi
    2047: chr(0x1D02F),  # 𝀯 Byzantine Musical Symbol Dyo
    2048: chr(0x1D030),  # 𝀰 Byzantine Musical Symbol Tria
    2049: chr(0x1D031),  # 𝀱 Byzantine Musical Symbol Tessera
    2050: chr(0x1D032),  # 𝀲 Byzantine Musical Symbol Kratimata
    2051: chr(0x1D033),  # 𝀳 Byzantine Musical Symbol Apeso
    2052: chr(0x1D034),  # 𝀴 Byzantine Musical Symbol Fthora
    2053: chr(0x1D035),  # 𝀵 Byzantine Musical Symbol Imifthora
    2054: chr(0x1D036),  # 𝀶 Byzantine Musical Symbol Tromikon
    2055: chr(0x1D037),  # 𝀷 Byzantine Musical Symbol Katava
    2056: chr(0x1D038),  # 𝀸 Byzantine Musical Symbol Pelaston
    2057: chr(0x1D039),  # 𝀹 Byzantine Musical Symbol Psifiston
    2058: chr(0x1D03A),  # 𝀺 Byzantine Musical Symbol
    2059: chr(0x1D03B),  # 𝀻 Byzantine Musical Symbol
    2060: chr(0x1D03C),  # 𝀼 Byzantine Musical Symbol Rapisma
    2061: chr(0x1D03D),  # 𝀽 Byzantine Musical Symbol
    2062: chr(0x1D03E),  # 𝀾 Byzantine Musical Symbol Paraklitiki
    2063: chr(0x1D03F),  # 𝀿 Byzantine Musical Symbol Ichadin
    2064: chr(0x1D040),  # 𝁀 Byzantine Musical Symbol Nana
    2065: chr(0x1D041),  # 𝁁 Byzantine Musical Symbol Petasma
    2066: chr(0x1D042),  # 𝁂 Byzantine Musical Symbol
    2067: chr(0x1D043),  # 𝁃 Byzantine Musical Symbol Tromikon
    2068: chr(0x1D044),  # 𝁄 Byzantine Musical Symbol
    2069: chr(0x1D045),  # 𝁅 Byzantine Musical Symbol
    2070: chr(0x1D046),  # 𝁆 Byzantine Musical Symbol Ison Neo
    2071: chr(0x1D047),  # 𝁇 Byzantine Musical Symbol Oligon
    2072: chr(0x1D048),  # 𝁈 Byzantine Musical Symbol Oxeia
    2073: chr(0x1D049),  # 𝁉 Byzantine Musical Symbol Petasti
    2074: chr(0x1D04A),  # 𝁊 Byzantine Musical Symbol Koufisma
    2075: chr(0x1D04B),  # 𝁋 Byzantine Musical Symbol
    2076: chr(0x1D04C),  # 𝁌 Byzantine Musical Symbol
    2077: chr(0x1D04D),  # 𝁍 Byzantine Musical Symbol Pelaston
    2078: chr(0x1D04E),  # 𝁎 Byzantine Musical Symbol
    2079: chr(0x1D04F),  # 𝁏 Byzantine Musical Symbol Kentima
    2080: chr(0x1D050),  # 𝁐 Byzantine Musical Symbol Ypsili
    2081: chr(0x1D051),  # 𝁑 Byzantine Musical Symbol
    2082: chr(0x1D052),  # 𝁒 Byzantine Musical Symbol
    2083: chr(0x1D053),  # 𝁓 Byzantine Musical Symbol Yporroi
    2084: chr(0x1D054),  # 𝁔 Byzantine Musical Symbol
    2085: chr(0x1D055),  # 𝁕 Byzantine Musical Symbol Elafron
    2086: chr(0x1D056),  # 𝁖 Byzantine Musical Symbol Chamili
    2087: chr(0x1D057),  # 𝁗 Byzantine Musical Symbol Mikron
    2088: chr(0x1D058),  # 𝁘 Byzantine Musical Symbol Vareia
    2089: chr(0x1D059),  # 𝁙 Byzantine Musical Symbol Piasma
    2090: chr(0x1D05A),  # 𝁚 Byzantine Musical Symbol Psifiston
    2091: chr(0x1D05B),  # 𝁛 Byzantine Musical Symbol Omalon
    2092: chr(0x1D05C),  # 𝁜 Byzantine Musical Symbol
    2093: chr(0x1D05D),  # 𝁝 Byzantine Musical Symbol Lygisma
    2094: chr(0x1D05E),  # 𝁞 Byzantine Musical Symbol Paraklitiki
    2095: chr(0x1D05F),  # 𝁟 Byzantine Musical Symbol
    2096: chr(0x1D060),  # 𝁠 Byzantine Musical Symbol Eteron
    2097: chr(0x1D061),  # 𝁡 Byzantine Musical Symbol Kylisma
    2098: chr(0x1D062),  # 𝁢 Byzantine Musical Symbol
    2099: chr(0x1D063),  # 𝁣 Byzantine Musical Symbol Tromikon
    2100: chr(0x1D064),  # 𝁤 Byzantine Musical Symbol
    2101: chr(0x1D065),  # 𝁥 Byzantine Musical Symbol Synagma
    2102: chr(0x1D066),  # 𝁦 Byzantine Musical Symbol Syrma
    2103: chr(0x1D067),  # 𝁧 Byzantine Musical Symbol
    2104: chr(0x1D068),  # 𝁨 Byzantine Musical Symbol
    2105: chr(0x1D069),  # 𝁩 Byzantine Musical Symbol Seisma
    2106: chr(0x1D06A),  # 𝁪 Byzantine Musical Symbol Xiron
    2107: chr(0x1D06B),  # 𝁫 Byzantine Musical Symbol
    2108: chr(0x1D06C),  # 𝁬 Byzantine Musical Symbol
    2109: chr(0x1D06D),  # 𝁭 Byzantine Musical Symbol
    2110: chr(0x1D06E),  # 𝁮 Byzantine Musical Symbol
    2111: chr(0x1D06F),  # 𝁯 Byzantine Musical Symbol
    2112: chr(0x1D070),  # 𝁰 Byzantine Musical Symbol
    2113: chr(0x1D071),  # 𝁱 Byzantine Musical Symbol
    2114: chr(0x1D072),  # 𝁲 Byzantine Musical Symbol
    2115: chr(0x1D073),  # 𝁳 Byzantine Musical Symbol
    2116: chr(0x1D074),  # 𝁴 Byzantine Musical Symbol Eteron
    2117: chr(0x1D075),  # 𝁵 Byzantine Musical Symbol
    2118: chr(0x1D076),  # 𝁶 Byzantine Musical Symbol
    2119: chr(0x1D077),  # 𝁷 Byzantine Musical Symbol
    2120: chr(0x1D078),  # 𝁸 Byzantine Musical Symbol Thema
    2121: chr(0x1D079),  # 𝁹 Byzantine Musical Symbol Thes Kai
    2122: chr(0x1D07A),  # 𝁺 Byzantine Musical Symbol
    2123: chr(0x1D07B),  # 𝁻 Byzantine Musical Symbol
    2124: chr(0x1D07C),  # 𝁼 Byzantine Musical Symbol Yfen
    2125: chr(0x1D07D),  # 𝁽 Byzantine Musical Symbol Yfen Ano
    2126: chr(0x1D07E),  # 𝁾 Byzantine Musical Symbol Stavros
    2127: chr(0x1D07F),  # 𝁿 Byzantine Musical Symbol Klasma
    2128: chr(0x1D080),  # 𝂀 Byzantine Musical Symbol Dipli
    2129: chr(0x1D081),  # 𝂁 Byzantine Musical Symbol Kratima
    2130: chr(0x1D082),  # 𝂂 Byzantine Musical Symbol Kratima
    2131: chr(0x1D083),  # 𝂃 Byzantine Musical Symbol Kratima
    2132: chr(0x1D084),  # 𝂄 Byzantine Musical Symbol
    2133: chr(0x1D085),  # 𝂅 Byzantine Musical Symbol Apli
    2134: chr(0x1D086),  # 𝂆 Byzantine Musical Symbol Dipli
    2135: chr(0x1D087),  # 𝂇 Byzantine Musical Symbol Tripli
    2136: chr(0x1D088),  # 𝂈 Byzantine Musical Symbol Tetrapli
    2137: chr(0x1D089),  # 𝂉 Byzantine Musical Symbol Koronis
    2138: chr(0x1D08A),  # 𝂊 Byzantine Musical Symbol Leimma
    2139: chr(0x1D08B),  # 𝂋 Byzantine Musical Symbol Leimma
    2140: chr(0x1D08C),  # 𝂌 Byzantine Musical Symbol Leimma
    2141: chr(0x1D08D),  # 𝂍 Byzantine Musical Symbol Leimma
    2142: chr(0x1D08E),  # 𝂎 Byzantine Musical Symbol Leimma
    2143: chr(0x1D08F),  # 𝂏 Byzantine Musical Symbol Gorgon
    2144: chr(0x1D090),  # 𝂐 Byzantine Musical Symbol Gorgon
    2145: chr(0x1D091),  # 𝂑 Byzantine Musical Symbol Gorgon
    2146: chr(0x1D092),  # 𝂒 Byzantine Musical Symbol Digorgon
    2147: chr(0x1D093),  # 𝂓 Byzantine Musical Symbol Digorgon
    2148: chr(0x1D094),  # 𝂔 Byzantine Musical Symbol Digorgon
    2149: chr(0x1D095),  # 𝂕 Byzantine Musical Symbol Digorgon
    2150: chr(0x1D096),  # 𝂖 Byzantine Musical Symbol Trigorgon
    2151: chr(0x1D097),  # 𝂗 Byzantine Musical Symbol Argon
    2152: chr(0x1D098),  # 𝂘 Byzantine Musical Symbol
    2153: chr(0x1D099),  # 𝂙 Byzantine Musical Symbol Diargon
    2154: chr(0x1D09A),  # 𝂚 Byzantine Musical Symbol Agogi
    2155: chr(0x1D09B),  # 𝂛 Byzantine Musical Symbol Agogi
    2156: chr(0x1D09C),  # 𝂜 Byzantine Musical Symbol Agogi
    2157: chr(0x1D09D),  # 𝂝 Byzantine Musical Symbol Agogi
    2158: chr(0x1D09E),  # 𝂞 Byzantine Musical Symbol Agogi
    2159: chr(0x1D09F),  # 𝂟 Byzantine Musical Symbol Agogi
    2160: chr(0x1D0A0),  # 𝂠 Byzantine Musical Symbol Agogi
    2161: chr(0x1D0A1),  # 𝂡 Byzantine Musical Symbol Agogi
    2162: chr(0x1D0A2),  # 𝂢 Byzantine Musical Symbol Martyria
    2163: chr(0x1D0A3),  # 𝂣 Byzantine Musical Symbol Martyria
    2164: chr(0x1D0A4),  # 𝂤 Byzantine Musical Symbol Martyria
    2165: chr(0x1D0A5),  # 𝂥 Byzantine Musical Symbol Martyria
    2166: chr(0x1D0A6),  # 𝂦 Byzantine Musical Symbol Martyria
    2167: chr(0x1D0A7),  # 𝂧 Byzantine Musical Symbol Martyria
    2168: chr(0x1D0A8),  # 𝂨 Byzantine Musical Symbol Martyria
    2169: chr(0x1D0A9),  # 𝂩 Byzantine Musical Symbol Martyria
    2170: chr(0x1D0AA),  # 𝂪 Byzantine Musical Symbol Martyria
    2171: chr(0x1D0AB),  # 𝂫 Byzantine Musical Symbol Martyria
    2172: chr(0x1D0AC),  # 𝂬 Byzantine Musical Symbol Isakia
    2173: chr(0x1D0AD),  # 𝂭 Byzantine Musical Symbol
    2174: chr(0x1D0AE),  # 𝂮 Byzantine Musical Symbol
    2175: chr(0x1D0AF),  # 𝂯 Byzantine Musical Symbol
    2176: chr(0x1D0B0),  # 𝂰 Byzantine Musical Symbol
    2177: chr(0x1D0B1),  # 𝂱 Byzantine Musical Symbol Martyria
    2178: chr(0x1D0B2),  # 𝂲 Byzantine Musical Symbol Martyria
    2179: chr(0x1D0B3),  # 𝂳 Byzantine Musical Symbol Martyria
    2180: chr(0x1D0B4),  # 𝂴 Byzantine Musical Symbol
    2181: chr(0x1D0B5),  # 𝂵 Byzantine Musical Symbol
    2182: chr(0x1D0B6),  # 𝂶 Byzantine Musical Symbol Enarxis
    2183: chr(0x1D0B7),  # 𝂷 Byzantine Musical Symbol Imifonon
    2184: chr(0x1D0B8),  # 𝂸 Byzantine Musical Symbol
    2185: chr(0x1D0B9),  # 𝂹 Byzantine Musical Symbol Fthora
    2186: chr(0x1D0BA),  # 𝂺 Byzantine Musical Symbol Fthora
    2187: chr(0x1D0BB),  # 𝂻 Byzantine Musical Symbol Fthora
    2188: chr(0x1D0BC),  # 𝂼 Byzantine Musical Symbol Fthora
    2189: chr(0x1D0BD),  # 𝂽 Byzantine Musical Symbol Fthora
    2190: chr(0x1D0BE),  # 𝂾 Byzantine Musical Symbol Fthora
    2191: chr(0x1D0BF),  # 𝂿 Byzantine Musical Symbol Fthora
    2192: chr(0x1D0C0),  # 𝃀 Byzantine Musical Symbol Fthora
    2193: chr(0x1D0C1),  # 𝃁 Byzantine Musical Symbol Fthora
    2194: chr(0x1D0C2),  # 𝃂 Byzantine Musical Symbol Fthora
    2195: chr(0x1D0C3),  # 𝃃 Byzantine Musical Symbol Fthora
    2196: chr(0x1D0C4),  # 𝃄 Byzantine Musical Symbol Fthora
    2197: chr(0x1D0C5),  # 𝃅 Byzantine Musical Symbol Fhtora
    2198: chr(0x1D0C6),  # 𝃆 Byzantine Musical Symbol Fthora
    2199: chr(0x1D0C7),  # 𝃇 Byzantine Musical Symbol Fthora
    2200: chr(0x1D0C8),  # 𝃈 Byzantine Musical Symbol Chroa
    2201: chr(0x1D0C9),  # 𝃉 Byzantine Musical Symbol Chroa
    2202: chr(0x1D0CA),  # 𝃊 Byzantine Musical Symbol Chroa
    2203: chr(0x1D0CB),  # 𝃋 Byzantine Musical Symbol Fthora I
    2204: chr(0x1D0CC),  # 𝃌 Byzantine Musical Symbol Fthora
    2205: chr(0x1D0CD),  # 𝃍 Byzantine Musical Symbol Yfesis
    2206: chr(0x1D0CE),  # 𝃎 Byzantine Musical Symbol Diesis
    2207: chr(0x1D0CF),  # 𝃏 Byzantine Musical Symbol Diesis
    2208: chr(0x1D0D0),  # 𝃐 Byzantine Musical Symbol Diesis
    2209: chr(0x1D0D1),  # 𝃑 Byzantine Musical Symbol Diesis
    2210: chr(0x1D0D2),  # 𝃒 Byzantine Musical Symbol Diesis
    2211: chr(0x1D0D3),  # 𝃓 Byzantine Musical Symbol Diesis
    2212: chr(0x1D0D4),  # 𝃔 Byzantine Musical Symbol Yfesis
    2213: chr(0x1D0D5),  # 𝃕 Byzantine Musical Symbol Yfesis
    2214: chr(0x1D0D6),  # 𝃖 Byzantine Musical Symbol Yfesis
    2215: chr(0x1D0D7),  # 𝃗 Byzantine Musical Symbol Yfesis
    2216: chr(0x1D0D8),  # 𝃘 Byzantine Musical Symbol Geniki
    2217: chr(0x1D0D9),  # 𝃙 Byzantine Musical Symbol Geniki
    2218: chr(0x1D0DA),  # 𝃚 Byzantine Musical Symbol Diastoli
    2219: chr(0x1D0DB),  # 𝃛 Byzantine Musical Symbol Diastoli
    2220: chr(0x1D0DC),  # 𝃜 Byzantine Musical Symbol Diastoli
    2221: chr(0x1D0DD),  # 𝃝 Byzantine Musical Symbol Diastoli
    2222: chr(0x1D0DE),  # 𝃞 Byzantine Musical Symbol Simansis
    2223: chr(0x1D0DF),  # 𝃟 Byzantine Musical Symbol Simansis
    2224: chr(0x1D0E0),  # 𝃠 Byzantine Musical Symbol Simansis
    2225: chr(0x1D0E1),  # 𝃡 Byzantine Musical Symbol Simansis
    2226: chr(0x1D0E2),  # 𝃢 Byzantine Musical Symbol Simansis
    2227: chr(0x1D0E3),  # 𝃣 Byzantine Musical Symbol Simansis
    2228: chr(0x1D0E4),  # 𝃤 Byzantine Musical Symbol Simansis
    2229: chr(0x1D0E5),  # 𝃥 Byzantine Musical Symbol Simansis
    2230: chr(0x1D0E6),  # 𝃦 Byzantine Musical Symbol
    2231: chr(0x1D0E7),  # 𝃧 Byzantine Musical Symbol Diftoggos
    2232: chr(0x1D0E8),  # 𝃨 Byzantine Musical Symbol Stigma
    2233: chr(0x1D0E9),  # 𝃩 Byzantine Musical Symbol Arktiko
    2234: chr(0x1D0EA),  # 𝃪 Byzantine Musical Symbol Arktiko
    2235: chr(0x1D0EB),  # 𝃫 Byzantine Musical Symbol Arktiko
    2236: chr(0x1D0EC),  # 𝃬 Byzantine Musical Symbol Arktiko Di
    2237: chr(0x1D0ED),  # 𝃭 Byzantine Musical Symbol Arktiko
    2238: chr(0x1D0EE),  # 𝃮 Byzantine Musical Symbol Arktiko
    2239: chr(0x1D0EF),  # 𝃯 Byzantine Musical Symbol Arktiko Ni
    2240: chr(0x1D0F0),  # 𝃰 Byzantine Musical Symbol
    2241: chr(0x1D0F1),  # 𝃱 Byzantine Musical Symbol Kentima
    2242: chr(0x1D0F2),  # 𝃲 Byzantine Musical Symbol
    2243: chr(0x1D0F3),  # 𝃳 Byzantine Musical Symbol Kentima
    2244: chr(0x1D0F4),  # 𝃴 Byzantine Musical Symbol Klasma
    2245: chr(0x1D0F5),  # 𝃵 Byzantine Musical Symbol Gorgon
}

test_value = 'e)Mo/lon *samfis s3jac #867'

def convert_betacode_to_unicode(string_value: str) -> str:
    output_value = []
    string_value = string_value.upper()
    capitalize_next = False
    for index, character_value in enumerate(string_value):
        new_character = ''
        if (index + 1) < len(string_value):
            next_value = string_value[index + 1]
        else:
            next_value = ' '
        if character_value in '*':
            capitalize_next = True
            continue
        all_chars = list(mappings.keys()) + ['#']
        if character_value not in all_chars:
            continue
        if character_value in 'S':
            # look ahead
            if next_value == '1':  # medial sigma
                new_character = chr(0x03C3)
            elif next_value in '2.,:;-_ ':  # final sigma
                new_character = chr(0x03C2)
            elif next_value == '3':  # lunate sigma
                new_character = chr(0x03F2)
            else:
                new_character = chr(0x03C3)
        elif character_value in '#':
            if next_value not in '0123456789':
                new_character = chr(0x0374)
            else:
                num_match = re.search(r'[0123456789]+', string_value[index:])
                if num_match:
                    special_char_number = num_match.group(0)
                    new_character = hash_mappings.get(int(special_char_number))
        else:
            new_character = mappings.get(character_value)
        if capitalize_next:
            new_character = new_character.upper()
            capitalize_next = False
        output_value.append(new_character)
    output_value = ''.join(output_value)
    output_value = unicodedata.normalize('NFC', output_value)
    return output_value

print(convert_betacode_to_unicode(test_value))
