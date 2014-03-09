# -*- coding: utf-8 -*-
"""
Module: test_runcards.py
Created on Thu Jan 09 21:10:42 2014
@author: gav
Description:

"""
### Imports
from __future__ import print_function

import pytest
import unittest

from datetime import datetime

from context import jack
from jack import runcards as rc

### Logging
import logging
logging.basicConfig(level=logging.DEBUG)
debug, info, error = logging.debug, logging.info, logging.error
### Constants

### Classes

### Fixtures

### Tests

def test_fail():
    assert False == False

def test_true_date():
    assert rc.true_date()

def test_random_date():
    start = datetime(2002, 1, 1)
    end   = datetime(2002, 12, 31)
    mydate = rc.random_date(start, end)
    assert start < mydate < end


if __name__ == "__main__":
    pytest.main(['test_runcards.py', '--cov-report', 'html', '--cov', '../jack/runcards.py', '-xvv'])
    # pytest.main(["--cov-report", "html", "--cov", "../jack", "../tests/", "-vv"])
#    pytest.main()




    print("Done __main__")
