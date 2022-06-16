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
curl  http://data.cabq.gov/airquality/aqindex/history/042222.0017  > data.dat
```



3. Run the program

```bash
python abqaq.py < data.dat
```
