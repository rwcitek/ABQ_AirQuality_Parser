""" util.py : Various utility functions and classes including custom errors. """
import sys
from options import options, parse_args


def argf():
    """argf : return the open input handle. stdin or open(argv[1]). Like Ruby ARGF"""
    if sys.stdin.isatty():
        return open(options['ifile'], newline="")
    else:
        return sys.stdin



def eprint(*args):
    """eprint like print but writes to stderr"""
    print(*args, file=sys.stderr)




def iprint(*args):
    """ like eprint, but checks agains the '--quiet' flag and suppresses the outout """
    if options['quiet']:
        pass
    else:
        eprint(*args)

