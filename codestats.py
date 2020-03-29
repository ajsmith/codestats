#!/usr/bin/env python
"""\
Analyze a source code file and provide statistics about it.

Currently this just checks for comments content using Java/C++ comment
style syntax. Maybe someday it'll do more.
"""

import re
import sys


def pct(n, m, ndigits=0):
    """Return the quotient of two numbers as a percentage."""
    return round(100 * n / float(m), ndigits)


def summarize(source, re_prog):
    """Display source code statistics."""
    comments = re_prog.findall(source)
    chunks = re_prog.split(source)
    comments_length = sum(len(s) for s in comments)
    source_length = len(source)
    code_length = source_length - comments_length
    comments_pct = pct(comments_length, source_length, 1)

    for (i, s) in zip(range(len(chunks)), chunks):
        is_comment = bool(re_prog.match(s))
        if is_comment:
            print('Chunk %d [COMMENT]:' % (i + 1))
        else:
            print('Chunk %d [CODE]:' % (i + 1))
        print (s + '\n')

    print('Summary')
    print('-------')
    print('total length: %d' % source_length)
    print('code length: %d' % code_length)
    print('comments length: %d' % comments_length)
    print('comments content percentage: %.1f%%' % comments_pct)


def main(argv=None):
    """The main part."""
    argv = argv or sys.argv
    filename = argv[1]
    multiline_prog = re.compile(r'(/\*.*?\*/|//.*?$)', (re.MULTILINE|re.DOTALL))

    with open(filename) as f:
        summarize(f.read(), multiline_prog)


if __name__ == '__main__':
    main()
