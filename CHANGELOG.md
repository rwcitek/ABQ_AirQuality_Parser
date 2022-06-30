# CHANGELOG

 0.1.0

## 2022-06-29

Corrected options.py to handle:

- If -c, --config given: no input file is needed and no error is reported
- Better help message for --help
- If .abqaq.yml is present then proper priority of options is computed if command line options present
- Refactored parse_args to get_flags and process_args for better testability

### Better error messages

- If parse error, now shows proper line and column numbers
- Opther exceptions are caught and better reported.

### Better docstrings for documentation

Note: much more work is needed here.

### Replaced data.json, data.yml

Since the default behaviour is now to output data friendly data sections in Locations,
the data.json and data.yml in the examples now reflect that format.

## 2022-06-28

- Added options.py : Command line options and argument parsing
- Added util.py : Refactored function from abqaq.py

Added '-c', '--config' flag to write out options to ./.abqaq.yml
If present, sets options for all runs 
if Options given override any set in .abq.yml

# 0.0.10

##2022-06-27

 Refactored code to be in options.py or util.py . Added --pretty which reverses previous default behaviour. Now data.yml, data.json have data normalized records, not human readable ones


# 0.0.9

## 2022-06-25

- Added -j, --json  to output JSON format.
