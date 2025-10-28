## Betacode to Unicode Converter for Suda Reader Application

This package implements a mapping of betacode characters to Unicode characters in the UTF-8 encoding 
that partially conforms to _The TLG® Betacode Manual_, 
© 2000 The Thesaurus Linguae Graecae®,
https://www.tlg.uci.edu/encoding/BCM.pdf, 
as updated December 23, 2023 and retrieved retrieved on October 27, 2025.

The following mapping tables have been incorporated thus far 
(those not incorporated at all are marked **NO**, 
those only incorporated in part are marked **PARTIAL** and linked to the implementing module,
and those completed are marked with a check mark and link to the incorporating module):

1. Alphabets and Basic Punctuation  
    1.1 [Greek](./betacode_converter.py) ✔  
    1.2 [Combining Diacritics](./betacode_converter.py) ✔  
    1.3 [Basic Punctuation](./betacode_converter.py) ✔  
    1.4 Latin  **NO**  
    1.5 Coptic  **NO**  
    1.6 Hebrew  **NO**  
    1.7 $ and & – Text Styles  **NO**  
2. Formatting Beta Codes  
    2.1 ^ and @ – Page Formatting  **NO**  
    2.2 { – Textual Mark-Up  **NO**  
    2.3 < – Text Formatting  **NO**  
3. Further punctuation and characters  
    3.1 " – Quotation Marks  **NO**  
    3.2 [ – Brackets  **NO**  
    3.3 % – Additional Punctuation and Characters  **NO**  
    3.4 # – [Additional Characters](./additional_character_mappings.py)  **PARTIAL**  

By default, the converted text is output as UTF-8 in Normalization Form C (NFC),
that is as pre-composed characters; via an optional parameter, the NFC normalization can be 
skipped, in which case the characters will output in Normalization Form D (NFD).

