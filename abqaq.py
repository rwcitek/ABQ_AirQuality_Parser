""" abaq.py : Attempt to parse data from Albuquerque, NM Air quality sensor data """
import sys
from parsy import seq, string, regex

# util functions


def argf():
    """argf : return the open input handle. stdin or open(argv[1]). Like Ruby ARGF"""
    if sys.stdin.isatty():
        return open(sys.argv[1], newline="")
    else:
        return sys.stdin


def iscrlf(slice):
    """checks if slice matches crlf terminal"""
    try:
        crlf.parse_partial(slice)
        return True
    except:
        return False


def eprint(*args):
    """eprint like print but writes to stderr"""
    print(*args, file=sys.stderr)


# helper functions
def mkfilesec(**kwargs):
    """Returns dictionary: {File: [{k,v}, ...] ...} with Group section  embeded"""
    return {"File": kwargs["Meta"], "Groups": kwargs["Groups"]}


def mkgroupsec(**kwargs):
    """returns group section: {'Group' [... group ...]}"""
    return {"Meta": kwargs["Meta"], "Data": kwargs["Data"]}


def mkdatasec(**kwargs):
    """Returns data section: {'Locations': ... CSVLine s .. }"""
    return {"Locations": kwargs["Locs"]}


def mkdict(**kwargs):
    """Converts key word arguments into key/value dictionary"""
    return {kwargs["key"]: kwargs["value"]}


# Terminals

cr = string("\r")
lf = string("\n")
crlf = cr + lf
el = lf | crlf  # Use this alias for the type of line endings. Orig file has Cr Lf el s
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

kv = seq(name=k1 << comma, site=id)
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

# Simplified KeyLine. A dict with a key and value of list of one or more values
#  KeyLine=seq(key=k1, value=(comma >> k1).at_least(1)).combine_dict(mkdict)
# will result: "foo,bar" => {'foo': ['bar']}; "foo,bar,baz" => {'foo': ['bar', 'bar', 'baz']
# ... "foo,bar,baz,spam,7" => {'foo': ['bar', 'baz', 'baz', 'spam', '7']

Value = k1


# This is the new line parse for CSV lines
CSVLine = seq(key=k1, value=(comma >> k1).at_least(1)).combine_dict(mkdict)
DataSection = seq(
    StartData=bd, Locs=(el >> CSVLine).at_least(1), EndData=(el >> ed << el)
).combine_dict(mkdatasec)

GroupSection = seq(
    GroupStart=bg,
    Meta=(el >> CSVLine).at_least(1),
    Data=(el >> DataSection),
    EndGroup=(eg << el),
).combine_dict(mkgroupsec)
GroupSectionList = el >> GroupSection.at_least(1)

FileSection = seq(
    File=bf,
    Meta=(el >> CSVLine).at_least(1),
    Groups=GroupSectionList,
    EndFile=(ef << el),
).combine_dict(mkfilesec)


def main():
    """Read from argv[1] or stdin and try to parse it"""
    try:
        with argf() as f:
            x = f.read()
            if iscrlf(x[10:12]):
                eprint("Input has Cr Lf line endings")
            print(FileSection.parse(x))
    except Exception as exc:
        eprint(
            "Line and column numbers are 0-indexed. E.g. 0:10 would be line 1, col 9",
            exc,
        )
        exit(1)


if __name__ == "__main__":
    main()
