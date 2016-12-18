#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" stdinfile.py
    Reads stdin, writes to a temp file, and prints the temp file name.
    For use with bash's process substitution:

pygments -l python -f html -O full stdinfile.py | google-chrome "$(stdinfile)"

    -Christopher Welborn 07-11-2015
"""

import os
import sys
import tempfile

from docopt import docopt

NAME = 'StdinFile'
VERSION = '0.0.2'
VERSIONSTR = '{} v. {}'.format(NAME, VERSION)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

USAGESTR = """{versionstr}

    Creates a temporary file from stdin input, and prints the file name.

    Usage:
        {script} [-h | -v]

    Options:
        -h,--help     : Show this help message.
        -v,--version  : Show version.
""".format(script=SCRIPT, versionstr=VERSIONSTR)


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    try:
        data = sys.stdin.buffer.read()
    except EnvironmentError as exr:
        print_err('Unable to read stdin: {}'.format(exr))
        return 1
    else:
        fname = write_temp_file(data)
        if fname:
            sys.stdout.write(fname)
            return 0
    return 1


def print_err(s):
    """ Print a line of text to stderr. """
    sys.stderr.write(''.join((s, '\n')))


def write_temp_file(rawbytes):
    """ Create a temp file, write rawbytes to it, and close it.
        Return the file name that was written, or None on failure.
        Errors are printed to stderr.
    """
    try:
        fd, fname = tempfile.mkstemp(
            suffix='.tmp',
            prefix='stdinfile.',
            dir=tempfile.gettempdir()
        )
    except EnvironmentError as ex:
        print_err('Unable to create a temp file: {}'.format(ex))
        return None

    try:
        os.write(fd, rawbytes)
    except IOError as exw:
        print_err('Failed to read stdin and write temp file: {}'.format(exw))
        return None
    else:
        os.close(fd)

    return fname


if __name__ == '__main__':
    mainret = main(docopt(USAGESTR, version=VERSIONSTR))
    sys.exit(mainret)
