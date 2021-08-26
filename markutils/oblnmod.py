import sys
import re

_verbadjadv_rx = re.compile('^[VAR]')
_substpronnum_rx = re.compile('^([NPM]|Y[np])')

def mark_obl(sentence: list) -> None:
    """
    - obl care nu au ca head verbe, adjective sau adverbe;
    """

    for parts in sentence:
        head = int(parts[6])
        drel = parts[7]

        if drel == 'obl' and head > 0:
            hmsd = sentence[head - 1][4]

            if not _verbadjadv_rx.match(hmsd):
                parts[0] = '!' + parts[0]
                print("obl -> {0}".format(hmsd), file=sys.stderr, flush=True)
            # end if
        # end if
    # end for


def mark_nmod(sentence: list) -> None:
    """
    - nmod care nu au ca head substantive, pronume sau numerale;
    """

    for parts in sentence:
        head = int(parts[6])
        drel = parts[7]

        if drel == 'nmod' and head > 0:
            hmsd = sentence[head - 1][4]

            if not _substpronnum_rx.match(hmsd):
                parts[0] = '!' + parts[0]
                print("nmod -> {0}".format(hmsd), file=sys.stderr, flush=True)
            # end if
        # end if
    # end for
