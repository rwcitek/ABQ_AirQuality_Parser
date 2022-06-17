""" abaq.py : Attempt to parse data from Albuquerque, NM Air quality sensor data """
import sys
from parsy import seq, string, regex

# util functions

def argf():
  """ argf : return the open input handle. stdin or open(argv[1]). Like Ruby ARGF """
  if sys.stdin.isatty():
    return open(sys.argv[1], newline='')
  else:
    return sys.stdin

def iscrlf(slice):
  """ checks if slice matches crlf terminal """
  try:
    crlf.parse_partial(slice)
    return True
  except:
    return False

def eprint(*args):
  """ eprint like print but writes to stderr """
  print(*args, file=sys.stderr)

# helper functions
def xclude_empties(*args):
    return [x for x in args if x is not None]


# Terminals

cr = string("\r")
lf = string("\n")
crlf = cr + lf
el = (lf | crlf)  # Use this alias for the type of line endings. Orig file has Cr Lf el s
caps = regex(r" *[A-Z]")

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
vl = (comma >> k1).many()
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
    """ Read from argv[1] or stdin and try to parse it """
    try:
        with argf() as f:
            x = f.read()
            if iscrlf(x[10:12]):
              eprint("Input has Cr Lf line endings")
            print(FileSection.parse(x))
    except Exception as exc:
        print("Line and column numbers are 0-indexed. E.g. 0:10 would be line 1, col 9", exc)
        exit(1)


if __name__ == "__main__":
    main()
