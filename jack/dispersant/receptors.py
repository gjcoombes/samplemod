#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Module: receptors.py
Package:
Created on Sun Mar 09 17:42:49 2014
@author: gav
Description:
Deals with receptors for the dispersant workflow
"""
### Imports
from __future__ import print_function, division

import geojson
from pprint import pprint, pformat

import banks.gis.tie as tie

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
def define_receptor_cmd(args):
    """
    Take the receptor from the tie file and write a single geojson file.

    This file will be a feature collection, probably of one polygon.
    """

    names = {
        'browse'   : 'Browse Island',
        'pinnacles': 'Pinnacles Bonaparte',
        'bare': 'Bare Sand Island',
    }
    print("Defining a receptor with:\n{}".format(pformat(args)))
    fp = args['tie_fp']
    out_fp = args['out_fp']
    key = args['<name>']
    receptor_name = names.get(key, key)
    feat_coll = tie.tie_feature_collection(fp)
    # Filter required feature into new collection
    feat = filter(lambda f: f['properties']['name'] == receptor_name,
                  feat_coll['features'])
    new_coll = geojson.FeatureCollection([feat])
    with open(out_fp, 'w') as sink:
        sink.write(geojson.dumps(new_coll, sort_keys=True))

### Tests

if __name__ == "__main__":

    print("Done __main__")
