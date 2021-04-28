import sys
import re
from . import fix_str_const, fix_str_const2, morphosyntactic_features

_num_rx = re.compile('^[0-9]+([.,][0-9]+)?$')
_int_rx = re.compile('^[0-9]+([.,][0-9]+)?(-|﹘|‐|‒|–|—)[0-9]+([.,][0-9]+)?$')
_romans = [
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII',
    'XIX', 'XX', 'XXI',  'XXII', 'XXIII', 'XXIV',  'XXV', 'XXVI',
    'XXVII', 'XXVIII',  'XXIX', 'XXX', 'XXXI', 'XXXII', 'XXXIII',
    'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 'XL',
    'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI', 'XLVII', 'XLVIII',
    'XLIX', 'L', 'LI', 'LII', 'LIII', 'LIV', 'LV', 'LVI', 'LVII',
    'LVIII', 'LIX', 'LX', 'LXI', 'LXII', 'LXIII', 'LXIV', 'LXV',
    'LXVI', 'LXVII', 'LXVIII', 'LXIX', 'LXX', 'LXXI', 'LXXII',
    'LXXIII', 'LXXIV', 'LXXV', 'LXXVI', 'LXXVII', 'LXXVIII',
    'LXXIX', 'LXXX', 'LXXXI', 'LXXXII', 'LXXXIII', 'LXXXIV',
    'LXXXV', 'LXXXVI', 'LXXXVII', 'LXXXVIII', 'LXXXIX', 'XC',
    'XCI', 'XCII', 'XCIII', 'XCIV', 'XCV', 'XCVI', 'XCVII',
    'XCVIII', 'XCIX', 'C'
]
_literal_nums = [
    'unu', 'doi', 'trei', 'patru', 'cinci', 'șase', 'șapte', 'opt',
    'nouă', 'zece', 'unsprezece', 'doisprezece', 'treisprezece',
    'paisprezece', 'cincisprezece', 'șaisprezece', 'șaptesprezece',
    'optsprezece', 'nouăsprezece', 'douăzeci', 'treizeci', 'patruzeci',
    'cincizeci', 'șaizeci', 'șaptezeci', 'optzeci', 'nouăzeci'
]
_literal_numbers_int_rx = re.compile(
    '(' + '|'.join(_literal_nums) + ')(-|﹘|‐|‒|–|—)(' + '|'.join(_literal_nums) + ')', re.IGNORECASE)
_bullet_rx = re.compile('^[0-9]+[a-zA-Z0-9.]+$')
_telephone_rx = re.compile('^0[0-9]+([.-]?[0-9])+$')


def fix_numerals(sentence: list) -> None:
    """Takes a list of CoNLL-U sentences are produced by conllu.read_conllu_file() and applies
    the numeral rules."""

    for parts in sentence:
        word = parts[1]
        msd = parts[4]
        performed = False

        if parts[3] != 'NUM':
            continue

        if (_num_rx.match(word) or _telephone_rx.match(word)) and msd != 'Mc-s-d':
            parts[4] = 'Mc-s-d'
            performed = True
        elif _int_rx.match(word) and msd != 'Mc-p-d':
            parts[4] = 'Mc-p-d'
            performed = True
        elif (word in _romans or word.upper() in _romans) and msd != 'Mo-s-r':
            parts[4] = 'Mo-s-r'
            performed = True
        elif (_bullet_rx.match(word) or '/CE' in word) and msd != 'Mc-s-b':
            parts[4] = 'Mc-s-b'

            if parts[5] != '_':
                parts[5] = parts[5] + "|NumForm=Combi"
            else:
                parts[5] = "NumForm=Combi"

            performed = True
        elif _literal_numbers_int_rx.match(word) and msd != 'Mc-p-l':
            parts[4] = 'Mc-p-l'
            performed = True
        # end if

        if performed:
            parts[2] = word

            if parts[4] in morphosyntactic_features:
                parts[5] = morphosyntactic_features[parts[4]]
            else:
                print(fix_str_const2.format(
                    fix_numerals.__name__, msd), file=sys.stderr, flush=True)

            print(fix_str_const.format(
                fix_numerals.__name__, word, msd, parts[4]), file=sys.stderr, flush=True)
    # end for
