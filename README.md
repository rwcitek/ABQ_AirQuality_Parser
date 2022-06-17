# AbqAq_Parser
Parser for Abq, N.M. Air Quality data format


## Abstract

This file: abqaq.py will parse a file downloaded from Abq N.M.'s web site for air quality readings

It currently just checks the syntax of the file.
If the data file parses correctly, it will output a badly formed AST (list of
lists) and exit with a 0 status code.


If there is some fault in the data file or the program itself, it prints an error message
on stderr and exits with a status code of 1.

## Setup

Note: If running on a Debian-derived system, replace the python and pips with python3 and pip3.

This program works best with Python version 3.10. It may work with older versions, but they have not been tested.

Note: This step is optional.

0. Create a virtual environment.

```bash
python -m venv .venv
```

1.  Install the dependancies

```bash
pip install -r requirements.txt
```

2. Dowload a data file

```bash
curl http://data.cabq.gov/airquality/aqindex/history/042222.0017 > data.dat
```



3. Run the program

```bash
python abqaq.py < data.dat
```


## Data Sources

### City of Albur, New Mexico website

- [https://www.cabq.gov](https://www.cabq.gov)



### Historical air quality data directory

- [http://data.cabq.gov/airquality/aqindex/history/](http://data.cabq.gov/airquality/aqindex/history/)

Note: This parser currently works with just the first block of files herein.
Later files have just linefeed line endings. Work is underway to make an
option to change the line ending match in the parser to be whatever you want.

And there are other changes not recognized by this parser currently. Work is underway
to address these bugs. Interestingly though, the FORMAT_VERSION key is still 2!

## Grammar

The grammar was reversed engineered from the sample files.  This is not ideal due
to unforseen changes in the actual data in other files. See note above.

This grammar is the 3rd attempt, at least. The grammar is represented in Extended
Backus Naur Format or EBNF. The varient used is the type that uses operators from
RegExpLand. E.g. '*', '+', '?' and parens for grouping.

This grammar is extracted from the file: 'abqaq.py'. It employs the the strategy
capturing all the terminals (that are not commaa or line endings) in elements
of a list and capturing the nonterminals as lists or lists of lists.


```EBNF
/* terminals are listed first and lowercase. Names should be self-explanatory
*/

<KeyValueOpt> ::= 

<DataLine ::=> 

<DataSection> ::= 

<GroupSection> ::= 

<GroupSectionList> ::= <GroupSection>+

<FileSection> ::= 
```

