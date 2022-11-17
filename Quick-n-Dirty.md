# Quick-n-Dirty converter

A quick and dirty way to convert the "Free Form" data on the ABQ website is to use `sed` to convert it to YAML.  Then convert the YAML to JSON.  It doesn't get all the items the BNF parser gets, but it's close.

## An example

### First: Fetch the data

```bash
curl -s -O http://data.cabq.gov/airquality/aqindex/history/042222.0017
```

### Second: turn into YAML
```bash
cat 042222.0017 |
sed -re '/^[A-Z]{3}/{ s/,/: / }' |
sed -e '{ s/ *,/,/ }' |
sed -e '/^BEGIN_DATA/,/END_DATA/{ s/^/- / }' |
sed -re '{ s/^- BEGIN_DATA/DATA:/ }' |
sed -re '{ /^- END_DATA/d }' |
sed -re '0,/BEGIN_GROUP/{ s/^(BEGIN_GROUP)/GROUPS:\n\1/ }' |
sed -e '/^BEGIN_GROUP/,/END_GROUP/{ s/^/  / }' |
sed -re '{ s/^  BEGIN_GROUP/- / }' |
sed -re '{ /^  END_GROUP/d }' |
sed -e '/^BEGIN_FILE/,/END_FILE/{ s/^/  / }' |
sed -re '{ s/^  BEGIN_FILE/- / }' |
sed -re '{ /^  END_FILE/d }' > 042222.0017.yaml
```

### Third: convert YAML into JSON
```bash
cat 042222.0017.yaml |
ruby -rjson -ryaml -e 'puts YAML::load(ARGF.read).to_json' |
jq . |
grep -v null, > 042222.0017.json
```

## Example data
See the [data folder](https://github.com/rwcitek/ABQ_AirQuality_Parser/tree/main/data) for the resulting YAML and JSON files.

