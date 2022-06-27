""" options.py : handle the command line flags and build up the options dict """
import argparse as ap

# helper functions

def compose_data(l1, l2):
    """ compose_data(l1, l2) : zips l1 with l2 and converts tuples to lists """
    return list(map(list, zip(list(l1), list(l2))))

# globals

options = {
    'ifile': None, 
    'quiet': False,
    'serializer': 'YAML',
    'pretty': compose_data,
}



def mk_formatter(pretty=False):
    """ mk_formatter: if pretty is True returns lambda that joins list with "," else just proper yaml or json data array """
    if pretty:
        return lambda l1, l2: str(compose_data(l1, l2))
    else:
        return compose_data

def parse_args():
    """ Parse the command line flags and sets the options global """
    parser = ap.ArgumentParser(description="Albuquerque Air Quality Parser")
    parser.add_argument('ifile')
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppresses informational messages")
    parser.add_argument('-j', '--json',action='store_true', help='Use JSON instead of YAML') 
    parser.add_argument('-p', '--pretty', action='store_true', help='Output the data output in a more human friendly manner')
    flags = parser.parse_args()
    options['ifile'] = flags.ifile
    options['quiet'] = flags.quiet
    if flags.json:
        options['serializer'] = 'JSON'
    options['pretty'] = mk_formatter(flags.pretty)

