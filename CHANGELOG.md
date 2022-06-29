# CHANGELOG

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
