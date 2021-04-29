import sys
from pathlib import Path
from fixutils import read_conllu_file
from fixutils.numerals import fix_numerals
from fixutils.words import fix_letters, fix_months, fix_to_be
from fixutils.syntax import fix_aux_pass, remove_todo, fix_nmod2obl
from fixutils.punctuation import add_space_after_no

if __name__ == '__main__':
    remove_spaces = False
    conllu_file = sys.argv[1]

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 fixall.py [-s] <.conllu file>", file=sys.stderr)
        exit(1)
    elif sys.argv[1] == '-s':
        remove_spaces = True
        conllu_file = sys.argv[2]
    # end if

    (corpus, _) = read_conllu_file(conllu_file)
    
    for (comments, sentence) in corpus:
        if remove_spaces:
            add_space_after_no(sentence, comments)

        fix_numerals(sentence)
        fix_letters(sentence)
        fix_months(sentence)
        fix_to_be(sentence)
        fix_aux_pass(sentence)
        remove_todo(sentence)
        fix_nmod2obl(sentence)
    # end all sentences

    output_file = Path(conllu_file)
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
