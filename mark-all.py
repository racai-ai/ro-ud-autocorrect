import sys
from pathlib import Path
from fixutils import read_conllu_file
from markutils.oblnmod import mark_nmod, mark_obl

if __name__ == '__main__':
    conllu_file = sys.argv[1]

    if len(sys.argv) != 2:
        print("Usage: python3 mark-all.py <.conllu file>", file=sys.stderr)
        exit(1)
    # end if

    (corpus, _) = read_conllu_file(conllu_file)

    for (comments, sentence) in corpus:
        mark_nmod(sentence)
        mark_obl(sentence)
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
