#!/usr/bin/env python
"""\
Analyze a source code file and provide statistics about it.

Currently this just checks for comments content using Java/C++ comment
style syntax. Maybe someday it'll do more.
"""

import os
import os.path
import re
import sys


def pct(n, m, ndigits=0):
    """Return the quotient of two numbers as a percentage."""
    return round(100 * n / float(m), ndigits)


def analyze(source, re_prog):
    """Return statistics for source code."""
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

    return {
        'source_length': source_length,
        'code_length': code_length,
        'comments_length': comments_length,
    }


def analyze_file(file_path, re_prog):
    """Return source code statistics for a source code file."""
    with open(file_path, 'rb') as f:
        return analyze(f.read().decode('utf8', 'ignore'), re_prog)


def find_files(parent_dir):
    """Recursively list files within a directory."""
    for (dir_path, dir_names, file_names) in os.walk(parent_dir):
        for file_name in file_names:
            yield os.path.join(dir_path, file_name)


def main(argv=None):
    """The main part."""
    argv = argv or sys.argv
    parent_dir = argv[1]
    multiline_prog = re.compile(r'(/\*.*?\*/|//.*?$)', (re.MULTILINE|re.DOTALL))

    source_files = (
        fpath for fpath in find_files(parent_dir)
        if fpath.endswith('.scala') or fpath.endswith('.java')
    )

    stats = []
    for fpath in source_files:
        print('Analyzing', fpath)
        stats.append(analyze_file(fpath, multiline_prog))

    source_total = sum(x['source_length'] for x in stats)
    code_total = sum(x['code_length'] for x in stats)
    comments_total = sum(x['comments_length'] for x in stats)
    comments_pct = pct(comments_total, source_total, 1)

    print('Summary')
    print('-------')
    print('total source: %d' % source_total)
    print('total code: %d' % code_total)
    print('total comments: %d' % comments_total)
    print('comments percentage: %.1f%%' % comments_pct)


if __name__ == '__main__':
    main()
