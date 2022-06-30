""" options.py : handle the command line flags and build up the options dict """
import sys
import os
import argparse as ap
import yaml

# constants

CONFIG_FILE = ".abqaq.yml"

# globals

default_options = {
    "quiet": False,
    "serializer": "YAML",
    "pretty": False,
}

options = default_options.copy()

ifile = None

# helper functions

# decorator that makes pretty output is specified in options
def prettymaybe(fn):
    def wrapper(*args, **kwargs):
        if options["pretty"]:
            return str(fn(*args, **kwargs))
        else:
            return fn(*args, **kwargs)

    return wrapper


@prettymaybe
def compose_data(l1, l2):
    """compose_data(l1, l2) : zips l1 with l2 and converts tuples to lists"""
    return list(map(list, zip(list(l1), list(l2))))


def write_config(n_options):
    """writes the options dict to './.abqaq.yml' in YAML format"""
    n_options = n_options.copy()
    with open(CONFIG_FILE, "w") as cfg:
        cfg.write(yaml.dump(n_options))
        print(f"Configuration written to {CONFIG_FILE}", file=sys.stderr)


def read_config():
    """reads the CONFIG_FILE if exists and returns options dict else returns returns default_options"""
    if os.path.exists(".abqaq.yml"):
        my_options = {}
        with open(CONFIG_FILE) as cf:
            my_options = yaml.safe_load(cf)

        return my_options
    else:
        return default_options


def get_flags():
    """Parse the command line flags and sets the global options"""
    parser = ap.ArgumentParser(
        prog="abqaq.py",
        description="Albuquerque Air Quality Parser",
        epilog="Parses file.dat or reads from stdin and converts to YAML(o JSON if '-j' flag given, and writes to stdout",
    )
    # parser.add_argument('ifile')
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppresses informational messages"
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Use JSON instead of YAML"
    )
    parser.add_argument(
        "-p",
        "--pretty",
        action="store_true",
        help="Output the data output in a more human friendly manner",
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        help=f"Write config file to {CONFIG_FILE} and exit",
    )
    parser.add_argument("-V", "--version", action="version", version="0.1.0")
    return parser.parse_known_args()


def options_from_flags(flags, z_options):
    """Given parsed flags, convert into options dict"""
    x_options = {}
    tf = {False: z_options["serializer"], True: "JSON"}
    x_options["pretty"] = flags.pretty or z_options["pretty"]
    x_options["quiet"] = flags.quiet or z_options["quiet"]
    x_options["serializer"] = tf[flags.json]
    return x_options


def process_args():
    """Actually parse the CLI arguments and return options dict"""
    flags, remains = get_flags()
    if flags.config:
        write_config(options_from_flags(flags, default_options))
        exit(0)
    my_options = read_config()
    inp = remains + [None]
    my_options = options_from_flags(flags, my_options)
    return my_options, inp


## debug things


def poptions():
    print(f"option printer: {options}")
