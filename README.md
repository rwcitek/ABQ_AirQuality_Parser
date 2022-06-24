# AbqAq_Parser
Parser for Albuquerque, N.M., Air Quality data format

## Abstract

This file: abqaq.py will parse a file downloaded from Albuquerque, N.M.'s web site for air quality readings.

If the file parses correctly, it will write a YAML formatted file to stdout.
If there are any problems or the input source does notparse, it will print
a message to stderr and exit with a non-zero exit code.


## Setup

**Note**: If running on a Debian-derived system, replace python and pip with python3 and pip3.

This program works best with Python version 3.10. It may work with older versions, but they have not been tested.

### Dependencies

- parsy : Parser cobinator library
- pyyaml : YAML package for Python


#### Parsy

This program relies on the 'parsy' Python package. 
- [https://github.com/python-parsy/parsy](https://github.com/python-parsy/parsy)

That package requires Python 3.6 or greater.

#### PyYaml

YAML support is provided by pyyaml:

- [https://pyyaml.org](https://pyyaml.org)

**Note**: This step is optional. If you do not use virtual environment, 'parsy'
and 'pyyml' will be installed in your current Python global packages.

0. Create a virtual environment.

```bash
python -m venv .venv
source ./.venv/bin/activate
```

**Note**: You can deactivate the virtual environment anytime by:

```bash
deactivate
```

1.  Install the dependancies

```bash
pip install -r requirements.txt
```

## Running the parser

2. Dowload a data file

```bash
curl http://data.cabq.gov/airquality/aqindex/history/042222.0017 > data.dat
```

3. Run the program

```bash
python abqaq.py data.dat
```

**Note**: data.dat can also be redirected to stdin. Or you can use curl:

```bash
curl http://data.cabq.gov/airquality/aqindex/history/042222.0017 | python abqaq.py -
```

**Note**: the format of the output is in YAML. The Python package used is:

- pyyaml

https://pyyaml.org/wiki/PyYAMLDocumentation

The flow_style is set to always use nested block syntax.

Here is a page that describes the 2 styles (block vs. flow):
- https://www.javatpoint.com/yaml-styles

## Sample output data

### IR (intermediate Representation) from first stage parser
[data.ir](data.ir)

### Transformed dictionary after second phase

[data.dct](data.dct)

### Final YAML output

[data.yml](data.yml)

## Usage

The program abqaq.py takes some optional flags and a possible path to a data file.
If you want to have abqaq.py read from a pipe or stdin, pass '-' as the file path.

### Flags

- '-q, --quiet' : Suppresses informational output on stderr like note regarding CrLf line endings.
- '-h, --help' : Prints the usage and help message and exits without actually doing anything.

## Data Sources

### City of Albuquerque, NM, website

- https://www.cabq.gov

### Historical air quality data directory

- http://data.cabq.gov/airquality/aqindex/history/

**Note**: Only 7 files from this directory have been checked.
Various changes have been noted and been addressed by making the parser more forgiven.
Most of these items have been due to either differences in the format of data section
value lists or some garbage data.

E.g. Instead of '0.9923', a single field might have '.9923'.

## Grammar

The grammar was reversed engineered from the sample files.  This is not ideal due
to unforseen changes in the actual data in other files. See note above.

This grammar is the 3rd attempt, at least. The grammar is represented in Extended
Backus Naur Format or EBNF. The varient used is the type that uses operators from
RegExpLand. E.g. '*', '+', '?' and parens for grouping.

This grammar is extracted from the file: 'abqaq.py'. It employs the strategy
capturing all the terminals (that are not commas or line endings) in elements
of a list and capturing the nonterminals as lists of lists of lists.


### Terminals

- comma ","
- el ("\r\n" | "\n")
- value   /[A-Za-z0-9._\-\/ ]+/


```EBNF
<CSVLine> ::= value (comma value)+

<DataSection> ::= "BEGIN_DATA" (el <CSVLine>)+ el "END_DATA"

<GroupSection> ::= "BEGIN_GROUP" (el <CSVLine>)+ <DataSection> el "END_GROUP"

<FileSection> ::= "BEGIN_FILE" (el <CSVLine>)+ (el <GroupSection>)+ el "END_FILE" el
```

### BNF Playground

This site was used to develop the EBNF used above.

- https://bnfplayground.pauliankline.com/



