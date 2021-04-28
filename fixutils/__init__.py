import sys
import os

_fix_str_const = "{0}: {1}/{2} -> {3}"
_fix_str_const2 = "{0}: attributes missing for MSD {1}"

def read_conllu_file(file: str) -> tuple:
    """Reads a CoNLL-U format file are returns it."""

    corpus = []
    attributes = {}

    with open(file, mode='r', encoding='utf-8') as f:
        comments = []
        sentence = []
        linecounter = 0

        for line in f:
            linecounter += 1
            line = line.strip()

            if line:
                if not line.startswith('#'):
                    parts = line.split()

                    if len(parts) == 10:
                        sentence.append(parts)
                        features = parts[5]
                        msd = parts[4]

                        if msd not in attributes:
                            attributes[msd] = features
                    else:
                        raise RuntimeError(
                            "CoNLL-U line not well formed at line {0!s} in file {1}".format(linecounter, file), file=sys.stderr)
                else:
                    comments.append(line)
            elif sentence:
                corpus.append((comments, sentence))
                sentence = []
                comments = []
        # end for line
    # end with

    return (corpus, attributes)


# This needs to sit alongside Romanin UD treebanks repositories, checked out in the same folder
# as the 'ro-ud-autocorrect' repository!
(_, attributes_train) = read_conllu_file(
    os.path.join('..', '..', 'UD_Romanian-RRT', 'ro_rrt-ud-train.conllu'))
(_, attributes_dev) = read_conllu_file(
    os.path.join('..', '..', 'UD_Romanian-RRT', 'ro_rrt-ud-dev.conllu'))
(_, attributes_test) = read_conllu_file(
    os.path.join('..', '..', 'UD_Romanian-RRT', 'ro_rrt-ud-test.conllu'))
