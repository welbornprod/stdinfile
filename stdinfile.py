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
VERSION = '0.2.0'
VERSIONSTR = '{} v. {}'.format(NAME, VERSION)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

DEFAULT_TMP_DIR = tempfile.gettempdir()
DEFAULT_TMP_EXT = '.tmp'

USAGESTR = """{versionstr}

    Creates a temporary file from stdin input, and prints the file name.

    Usage:
        {script} [-h | -v]
        {script} [-d dir] [-e ext]

    Options:
        -d dir,--dir dir        : Temporary directory to use.
                                  Default: {default_tmp_dir}
        -e ext,--extension ext  : Extension for temporary file.
                                  Default: {default_extension}
        -h,--help               : Show this help message.
        -v,--version            : Show version.
""".format(
    default_extension=DEFAULT_TMP_EXT,
    default_tmp_dir=DEFAULT_TMP_DIR,
    script=SCRIPT,
    versionstr=VERSIONSTR,
)


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    tempdir = argd['--dir'] or DEFAULT_TMP_DIR
    if not os.path.isdir(tempdir):
        raise InvalidArg('Invalid temp. directory: {}'.format(tempdir))

    try:
        data = sys.stdin.buffer.read()
    except EnvironmentError as exr:
        print_err('Unable to read stdin: {}'.format(exr))
        return 1
    else:
        fname = write_temp_file(
            data,
            tempdir=tempdir,
            extension=argd['--extension']
        )
        if fname:
            sys.stdout.write(fname)
            return 0
    return 1


def print_err(*args, **kwargs):
    """ A wrapper for print() that uses stderr by default. """
    if kwargs.get('file', None) is None:
        kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def write_temp_file(rawbytes, tempdir=None, extension=None):
    """ Create a temp file, write rawbytes to it, and close it.
        Return the file name that was written, or None on failure.
        Errors are printed to stderr.
    """
    try:
        fd, fname = tempfile.mkstemp(
            suffix=extension or DEFAULT_TMP_EXT,
            prefix='stdinfile.',
            dir=tempdir or DEFAULT_TMP_DIR,
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


class InvalidArg(ValueError):
    """ Raised when the user has used an invalid argument. """
    def __init__(self, msg=None):
        self.msg = msg or ''

    def __str__(self):
        if self.msg:
            return 'Invalid argument, {}'.format(self.msg)
        return 'Invalid argument!'


if __name__ == '__main__':
    try:
        mainret = main(docopt(USAGESTR, version=VERSIONSTR))
    except InvalidArg as ex:
        print_err(ex)
        mainret = 1
    except (EOFError, KeyboardInterrupt):
        print_err('\nUser cancelled.\n')
        mainret = 2
    except BrokenPipeError:
        print_err('\nBroken pipe, input/output was interrupted.\n')
        mainret = 3
    sys.exit(mainret)
