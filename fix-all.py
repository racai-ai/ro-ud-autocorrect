import sys
from pathlib import Path
from fixutils import read_conllu_file
from fixutils.numerals import fix_numerals
from fixutils.words import fix_letters, fix_months, fix_to_be
from fixutils.syntax import fix_aux_pass, remove_todo, fix_nmod2obl

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 fixall.py <.conllu file>", file=sys.stderr)
        exit(1)
    # end if

    (corpus, _) = read_conllu_file(sys.argv[1])
    
    for (comments, sentence) in corpus:
        fix_numerals(sentence)
        fix_letters(sentence)
        fix_months(sentence)
        fix_to_be(sentence)
        fix_aux_pass(sentence)
        remove_todo(sentence)
        fix_nmod2obl(sentence)
    # end all sentences

    output_file = Path(sys.argv[1])
    output_file = Path(output_file.parent) / Path(output_file.name + ".fixed")

    with open(output_file, mode='w', encoding='utf-8') as f:
        for (comments, sentence) in corpus:
            f.write('\n'.join(comments))
            f.write('\n')
            f.write('\n'.join(['\t'.join(x) for x in sentence]))
            f.write('\n')
            f.write('\n')
        # end for
    # end with
