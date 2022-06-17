""" abaq.py : Attempt to parse data from Albuquerque, NM Air quality sensor data """
import sys
from parsy import seq, string, regex


# helper functions
def xclude_empties(*args):
    return [x for x in args if x is not None]


# Terminals

cr = string("\r")
lf = string("\n")
crlf = cr + lf
el = crlf  # Use this alias for the type of line endings. Orig file has Cr Lf el s
caps = regex(r"[A-Z]")

## Terminal literals

bd = string("BEGIN_DATA")
ed = string("END_DATA")
bg = string("BEGIN_GROUP")
eg = string("END_GROUP")
bf = string("BEGIN_FILE")
ef = string("END_FILE")


# TODO: Rename k1 to Key
k1 = regex(r"[A-Za-z0-9._\-\/ ]+")
id = regex(r"[0-9]+")
comma = string(",")
num = regex(r"-?[0-9]+(\.[0-9]+)?")

#  combined parsers

kv = seq(k1 << comma, id)
# the difference between '<<' and '>>' opers is: which side of the  oper is preserved in seq()
# If you want to exclude the leading ',' then >>. Or if it is a trailing then <<
#  IOW: the angles point to the thing you want to preserve
# The .many() turns into a regex-like '*' operation
vl = (comma >> num).many()
vc = (comma >> caps).many()

# Debug stuff here
def rddata(fn):
    """rddata() returns the _ exact _ contenst of 'begin_data.ex1'"""
    with open(fn, newline="") as f:  # Suppress the line ending handler
        return f.read()


# dbg = (bd >> lf >> seq(k1 << comma, num) + vlist << lf >> seq(k1 << comma, num) + vlist << lf << ed)
v = (comma >> num).many()
dbg = seq(bd, lf, k1, comma, num, v, lf, k1, comma, num, v, lf, ed)

# NonTerminals
Value = k1

# This captures the TZONE,MST,7 in the original file
KeyValueOpt = seq(k1, comma >> Value, (comma >> Value).optional()).combine(
    xclude_empties
)


DataLine = seq(el >> kv, vl, el >> kv, vc).at_least(1)
DataSection = seq(bd, DataLine, el >> ed << el)

GroupSection = seq(bg, (el >> KeyValueOpt).at_least(1), el >> DataSection, eg << el)
GroupSectionList = GroupSection.at_least(1)

FileSection = seq(bf, (el >> KeyValueOpt).at_least(1), el >> GroupSectionList, ef << el)


def main():
    x = sys.stdin.read()
    try:
        print(FileSection.parse(x))
    except Exception as exc:
        print(exc, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
