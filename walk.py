""" walk.py : walks the IR and productes dict which can be fed into YAML """
from functools import reduce


def unwrap_value(v, sep=":"):
    """given a value from IR key/value_list unwraps its value into a string with sep"""
    return sep.join(v)


def normalize(dicts):
    """normalize a list of dicts into a single dict"""
    return {k: unwrap_value(v) for k, v in reduce(lambda i, j: i | j, dicts).items()}


def fmt_val(tup):
    """given a tuple of the form : (0.9876, 'G') returns "[0.9876, G]" """
    return f"[{tup[0]}, {tup[1]}]"


def get_site(chk1, chk2):
    res = {}
    res["site"] = list(chk1.values())[0][0]
    res["name"] = list(chk1.keys())[0]
    l1 = list(chk1.values())[0][1:]
    l2 = list(chk2.values())[0][1:]
    res["data"] = ",".join(list(map(fmt_val, zip(l1, l2))))
    return res


# debug
def mkchk(site, name, data1, data2):
    return [{name: [site, *data1]}, {name: [site, *data2]}]


def get_data(chks):
    return [get_site(chks[i], chks[i + 1]) for i in range(0, len(chks), 2)]


def get_group(grp):
    res = {}
    res["Meta"] = grp["Meta"]
    res["Locations"] = get_data(grp["Data"]["Locations"])
    return res


# start here
def proc_ir(ir):
    """process the IR (Internal Representation) returned from parser. Returns a new dict"""
    res = normalize(ir["File"])
    res["Groups"] = [get_group(x) for x in ir["Groups"]]
    return res


if __name__ == "__main__":
    pass
