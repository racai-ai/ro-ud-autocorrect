import sys
import re

_todo_rx = re.compile('ToDo=([^|_]+)')

def fix_aux_pass(sentence: list, attrs: dict) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that if an aux:pass is present the subject is also passive."""

    auxpass_head = 0

    for parts in sentence:
        drel = parts[7]
        head = int(parts[6])

        if drel == 'aux:pass':
            auxpass_head = head
            break
        # end if
    # end for

    if auxpass_head > 0:
        for parts in sentence:
            drel = parts[7]
            head = int(parts[6])

            if drel.startswith('nsubj') and drel != 'nsubj:pass' and head == auxpass_head:
                parts[7] = 'nsubj:pass'
                print("{0}: nsubj -> nsubj:pass".format(fix_aux_pass.__name__),
                      file=sys.stderr, flush=True)
            elif drel.startswith('csubj') and drel != 'csubj:pass' and head == auxpass_head:
                parts[7] = 'csubj:pass'
                print("{0}: csubj -> csubj:pass".format(fix_aux_pass.__name__),
                      file=sys.stderr, flush=True)
            # end if
        # end for
    # end if

def remove_todo(sentence: list, attrs: dict) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that ToDo=... is removed if syntactic relation has been changed."""

    for parts in sentence:
        drel = parts[7]
        misc = parts[9]

        if 'ToDo' in misc:
            m = _todo_rx.search(misc)

            if m:
                rel = m.group(1)

                if drel == rel:
                    attr = 'ToDo=' + rel
                    misc = misc.replace(attr, '')
                    misc = misc.replace('||', '|')

                    if misc.startswith('|'):
                        misc = misc[1:]
                    
                    if misc.endswith('|'):
                        misc = misc[:-1]

                    if not misc:
                        misc = '_'
                    
                    print("{0}: {1} -> {2}".format(remove_todo.__name__, parts[9], misc),
                          file=sys.stderr, flush=True)
                    parts[9] = misc
                # end replace condition
            # end if m
        # end if ToDo
    # end parts


def fix_nmod2obl(sentence: list, attrs: dict) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that nmod -> obl when nmod is headed by a verb."""

    for parts in sentence:
        drel = parts[7]
        head = int(parts[6])

        if drel == 'nmod' and head > 0 and sentence[head - 1][3] == 'VERB':
            parts[7] = 'obl'
            print("{0}: nmod -> obl".format(fix_nmod2obl.__name__),
                    file=sys.stderr, flush=True)
        # end if
    # end for
