import sys
import fixutils

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 fixall.py <.conllu file>", file=sys.stderr)
        exit(1)
    # end if

    (corpus, msd2attr) = fixutils.read_conllu_file(sys.argv[1])
    
    for (comments, sentence) in corpus:
        fixutils.numerals.fix_numerals(sentence, msd2attr)
        fixutils.words.fix_letters(sentence, msd2attr)
        fixutils.words.fix_months(sentence, msd2attr)
        fixutils.words.fix_to_be(sentence, msd2attr)
        fixutils.syntax.fix_aux_pass(sentence, msd2attr)
        fixutils.syntax.remove_todo(sentence, msd2attr)
        fixutils.syntax.fix_nmod2obl(sentence, msd2attr)
    # end all sentences
