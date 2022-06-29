""" abaq.py : Attempt to parse data from Albuquerque, NM Air quality sensor data """
import sys
from parsy import seq, string, regex, ParseError
import yaml
from options import options, get_flags, process_args,  ifile
from util import argf, eprint, iprint
from walk import proc_ir

# Globals


# util functions


def serialize(ir2):
    """ Given IR dictionary from phase II, return string based on the value of options['serializer']. YAML | JSON """
    if options['serializer'] == 'JSON':
        from io import StringIO
        import json
        s = StringIO()
        json.dump(ir2, s)
        return s.getvalue()
    else:
        return yaml.dump(ir2,default_flow_style=False, sort_keys=False) 

def iscrlf(slice):
    """checks if slice matches crlf terminal"""
    try:
        crlf.parse_partial(slice)
        return True
    except:
        return False



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
comma = string(",")
cr = string("\r")
lf = string("\n")
crlf = cr + lf
el = lf | crlf  # el can be either a CrLf line ending or a Lf ending. Parse works for both

## Terminal literals

bd = string("BEGIN_DATA")
ed = string("END_DATA")
bg = string("BEGIN_GROUP")
eg = string("END_GROUP")
bf = string("BEGIN_FILE")
ef = string("END_FILE")


value = regex(r"[A-Za-z0-9._\-\/ ]+")
#num = regex(r"-?[0-9]+(\.[0-9]+)?")

#  combined parsers

kv = seq(name=value << comma, site=id)
# the difference between '<<' and '>>' opers is: which side of the  oper is preserved in seq()
# If you want to exclude the leading ',' then >>. Or if it is a trailing then <<
#  IOW: the angles point to the thing you want to preserve
# The .many() turns into a regex-like '*' operation
vl = (comma >> value).many()

# Debug stuff here
def rddata(fn):
    """rddata() returns the _ exact _ contenst of 'begin_data.ex1'"""
    with open(fn, newline="") as f:  # Suppress the line ending handler
        return f.read()



# NonTerminals


# This is the new line parse for CSV lines
CSVLine = seq(key=value, value=(comma >> value).at_least(1)).combine_dict(mkdict)
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
    global options
    o, remains = process_args()
    options |= o
    ifile = remains[0]
    try:
        with argf(ifile) as f:
            x = f.read()
            if iscrlf(x[10:12]):
                iprint("Input has Cr Lf line endings")
            print(serialize(proc_ir(FileSection.parse(x))))
    except ValueError as vex:
        eprint(vex)
        exit(3)
    except ParseError as pex:
        ln, cm = map(int, pex.line_info().split(':'))
        ln += 1; cm += 1
        eprint(f"parse error at line:{ln}, column{cm}")
        exit(2)
    except Exception as exc:
        eprint("Unknown error occurred:", exc)
        exit(1)


if __name__ == "__main__":
    main()
