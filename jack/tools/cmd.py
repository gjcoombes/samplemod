#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Module: cmd.py
Package:
Created on Sun Mar 09 10:24:14 2014
@author: gav
Description:

Usage:  jack select max_conc
        jack select max_vol
        jack select min_time
        jack define receptor (<tie> --output <out> | --input <in>)

Options:
    -h --help               Show this screen
    -v --version            Show version
    -i --input <in>         Yaml input file
    -o --output <out>       Filename of output file [default: receptor.geojson]
"""
### Imports
from __future__ import print_function, division

from docopt import docopt
from pprint import pprint

### Logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
debug, info, error = logger.debug, logger.info, logger.error
### Constants

### Classes

### Functions
def main(args):
    pprint(args)

def cmd():
    args = docopt(__doc__, version="jack v0.1.0")
    main(args)



### Tests

if __name__ == "__main__":

    print("Done __main__")
