# Read data from given file and store word occurances

# system imports
import argparse
from clint.textui import colored, puts, indent


class WordInfo(object):
    """ Store the occurances and absolute positions of a word. """
    def __init__(self, index, seed):
        self.occurances = seed
        self.positions = [index]

    def increment(self):
        self.occurances += 1

    def save(self, index):
        self.positions.append(index)

    def __repr__(self):
        return 'occurances = {} : positions = {}'.format(
            self.occurances, self.positions)


def open_document(filename):
    # word -> WordInfo
    words = {}

    # List of tokens on initial pass.
    # Stores "raw" tokens (words) that may
    # still contain puncuation. Used to
    # restore the original sentence when doing
    # a context search.
    document = []

    with open(filename, 'r') as f:
        content = f.readlines()
        f.close()

    # Iterate over lines, split into tokens,
    # store the occurances and absolute position
    index = 0

    for line in content:
        tokens = line.strip().split()

        for w in tokens:
            _w = w.strip('(),.')

            if _w in words:
                info = words.get(_w)
                info.increment()
                info.save(index)
            else:
                words[_w] = WordInfo(index, 1)

            document.append(w)
            index += 1

    return words, document


if __name__ == '__main__':
    # Context searching.
    # Retrieve all sentences containing the given query string.
    ap = argparse.ArgumentParser(description='Search text files for given words and their contexts.')

    # required arguments: filename and query string
    ap.add_argument('filename')
    ap.add_argument('query')

    args = ap.parse_args()

    words, document = open_document(args.filename)
    info = words.get(args.query, None)

    if info:
        puts('search term: {}'.format(colored.red('{}'.format(args.query))))
        with indent(4, quote=' >'):
            puts('{}'.format(info))

        puts('')
        puts('context search results')
        puts('----------------------')
        for index in info.positions:
            # TODO, support '.', '!', '?'

            # Search backwards to beginning of sentence
            # Start from the index to ensure we handle the case
            # where our query is the first word.
            start = index
            while (start > 0) and (not document[start - 1].endswith('.')):
                start -= 1

            # Search forwards to end of sentence
            # If the query is the last word in the sentence,
            # we must check for a terminating character to prevent
            # grabbing the next sentence as well.
            size = len(document)
            end = index
            while (end < (size - 1)) and (not document[end].endswith('.')):
                end += 1

            # Print found sentence
            puts('{} : {}'.format(index, ' '.join(document[start:(end + 1)])))
            puts('')

    else:
        print 'cannot find any occurances of: {}'.format(args.query)

