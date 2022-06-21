""" main.py : test harness for parsing and writing the output of parsing ABQ Air Quality file """

import sys
import yaml
from abqaq import rddata, FileSection
from walk import proc_ir


def main():
  x = rddata(sys.argv[1])
  ir = FileSection.parse(x)
  #  print(yaml.dump(proc_ir(ir), default_flow_style=False, sort_keys=False))
  print(proc_ir(ir))
if __name__ == "__main__":
  main()