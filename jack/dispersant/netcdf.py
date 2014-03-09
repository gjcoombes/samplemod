#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Module: netcdf.py
Package: jack.dispersant
Created on Sun Mar 09 19:14:52 2014
@author: gav
Description:
Handle the interrogation of stoch and shore netcdf files for the
dispersant workflow
"""
### Imports
from __future__ import print_function, division

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
def select_max_conc_cmd(args):
    """
    Find the run with the highest surface concentration within the receptor
    """
    pass

### Tests

if __name__ == "__main__":

    print("Done __main__")
