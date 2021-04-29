import re

_paired_punct_left = '({[„'
_paired_punct_right = ')}]”'
_delete_prev_space_punct = ',:;.%'
# Patterns with UPOSes and punctuation in the middle.
# Empty string means any UPOS.
_delete_all_space_patterns_punct = [
    ['NUM', ',', 'NUM'],
    ['NUM', '-', 'NUM'],
    ['', '/', '']
]
_space_after_no_strconst = 'SpaceAfter=No'
_text_rx = re.compile('^#\\s*text\\s*=\\s*')


def _get_updated_misc(misc: str) -> str:
    if _space_after_no_strconst in misc:
        return misc
    elif misc == '_':
        return _space_after_no_strconst
    else:
        return misc + '|' + _space_after_no_strconst


def add_space_after_no(sentence: list, comments: list) -> None:
    """Takes a sentence as returned by conll.read_conllu_file() and makes
    sure that all artificially inserted spaces around punctuation is removed."""

    paired_stack = []

    for i in range(len(sentence)):
        prev_parts = None
        prev_misc = None
        next_parts = None
        next_misc = None

        if i > 0:
            prev_parts = sentence[i - 1]
            prev_misc = prev_parts[9]
        
        if i < len(sentence) - 1:
            next_parts = sentence[i + 1]
            next_misc = next_parts[9]

        parts = sentence[i]
        word = parts[1]
        misc = parts[9]
        msd = parts[4]
        upos = parts[3]
        head = parts[6]

        # 1. Deal with paired punctuation
        if word in _paired_punct_left:
            parts[9] = _get_updated_misc(misc)
        elif word in _paired_punct_right and prev_parts:
            prev_parts[9] = _get_updated_misc(prev_misc)
        elif word == '"':
            if paired_stack and paired_stack[-1] == '"':
                prev_parts[9] = _get_updated_misc(prev_misc)
                paired_stack.pop()
            else:
                parts[9] = _get_updated_misc(misc)
                paired_stack.append(word)
        elif word == "'":
            if paired_stack and paired_stack[-1] == "'":
                prev_parts[9] = _get_updated_misc(prev_misc)
                paired_stack.pop()
            else:
                parts[9] = _get_updated_misc(misc)
                paired_stack.append(word)
        # end if

        # 2. Deal with previous spaces
        if word in _delete_prev_space_punct and prev_parts:
            prev_parts[9] = _get_updated_misc(prev_misc)

        # 3. Deal with Romanian clitics
        if word.endswith('-') and \
            (msd.endswith('y') or '-y-' in msd or \
            (next_parts and next_parts[4].startswith('V'))):
            parts[9] = _get_updated_misc(misc)

        if word.startswith('-') and \
            (upos == 'AUX' or upos == 'DET' or upos == 'ADP' or upos == 'PART') and prev_parts:
            prev_parts[9] = _get_updated_misc(prev_misc)

        # 3.1 Deal with noun compunds with '-'
        if word.endswith('-') and 'BioNERLabel=' in misc and \
            next_misc and 'BioNERLabel=' in next_misc:
            parts[9] = _get_updated_misc(misc)

        if word == '-' and head == prev_parts[0] and \
            next_parts and next_parts[6] == head:
            prev_parts[9] = _get_updated_misc(prev_misc)
            parts[9] = _get_updated_misc(misc)
    # end for

    # 4. Deal with patterns
    for patt in _delete_all_space_patterns_punct:
        for i in range(len(sentence) - len(patt)):
            ppi = -1

            for j in range(i, i + len(patt)):
                parts = sentence[j]
                upos = parts[3]
                word = parts[1]

                if patt[j - i] and upos != patt[j - i] and word != patt[j - i]:
                    # Pattern match fail
                    ppi = -1
                    break
                # end if

                if word == patt[j - i]:
                    ppi = j
                # end if
            # end for slice in sentece, for current pattern

            # Remove before and after spaces for this pattern
            if ppi >= 1:
                sentence[ppi][9] = _get_updated_misc(sentence[ppi][9])
                sentence[ppi - 1][9] = _get_updated_misc(sentence[ppi - 1][9])
            # end action if
        # end all slices of length of pattern
    # end all patterns

    new_text = []

    # 5. Redo the text = sentence
    for i in range(len(sentence)):
        parts = sentence[i]
        word = parts[1]
        misc = parts[9]

        if _space_after_no_strconst in misc or i == len(sentence) - 1:
            new_text.append(word)
        else:
            new_text.append(word + ' ')
        # end if
    # end for

    for i in range(len(comments)):
        if _text_rx.search(comments[i]):
            comments[i] = '# text = ' + ''.join(new_text)
            break
        # end if
    # end for
