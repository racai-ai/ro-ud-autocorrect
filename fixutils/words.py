import sys
import re
from . import fix_str_const, fix_str_const2, morphosyntactic_features

_letter_rx = re.compile('^[a-zA-ZșțăîâȘȚĂÎÂ]$')
_month_rx = re.compile('^(ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|noiembrie|decembrie)$', re.IGNORECASE)

def fix_letters(sentence: list) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that all single-char letters are tagged with 'Ncms-n'."""

    for parts in sentence:
        word = parts[1]
        lemma = parts[2]
        msd = parts[4]

        if parts[3] != 'NOUN':
            continue

        if _letter_rx.match(word) and msd != 'Ncms-n' and lemma == word:
            # Do not change K -> Kelvin instances which are Yn!
            parts[4] = 'Ncms-n'

            if parts[4] in morphosyntactic_features:
                parts[5] = morphosyntactic_features[parts[4]]
            else:
                print(fix_str_const2.format(
                    fix_letters.__name__, msd), file=sys.stderr, flush=True)

            print(fix_str_const.format(
                fix_letters.__name__, word, msd, parts[4]), file=sys.stderr, flush=True)
        # end if
    # end for


def fix_months(sentence: list) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that all month names are tagged with 'Ncm--n'."""

    for parts in sentence:
        word = parts[1]
        msd = parts[4]

        if parts[3] != 'NOUN':
            continue

        if _month_rx.match(word) and msd != 'Ncm--n':
            parts[4] = 'Ncm--n'
            parts[2] = word

            if parts[4] in morphosyntactic_features:
                parts[5] = morphosyntactic_features[parts[4]]
            else:
                print(fix_str_const2.format(
                    fix_months.__name__, msd), file=sys.stderr, flush=True)

            print(fix_str_const.format(
                fix_months.__name__, word, msd, parts[4]), file=sys.stderr, flush=True)
        # end if
    # end for

def fix_to_be(sentence: list) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that 'a fi' 'cop' or 'aux' is 'Va...'."""

    for parts in sentence:
        word = parts[1]
        lemma = parts[2]
        msd = parts[4]
        drel = parts[7]

        if lemma != 'fi':
            continue

        if (drel == 'aux' or drel == 'cop') and not msd.startswith('Va'):
            parts[4] = 'Va' + msd[2:]
            parts[3] = 'AUX'

            if parts[4] in morphosyntactic_features:
                parts[5] = morphosyntactic_features[parts[4]]
            else:
                print(fix_str_const2.format(
                    fix_to_be.__name__, msd), file=sys.stderr, flush=True)

            print(fix_str_const.format(
                fix_to_be.__name__, word, msd, parts[4]), file=sys.stderr, flush=True)
        # end if
    # end for
