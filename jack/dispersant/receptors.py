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
        'vernon': 'Vernon Islands CR',
        'indian': 'Indian Island CR',
        'beagle': 'Beagle Gulf - Darwin',
    }
    print("Defining a receptor with:\n{}".format(pformat(args)))
    fp = args['tie_fp']
    out_fp = args['out_fp']
    key = args['<name>']
    receptor_name = names.get(key, key)
    feat_coll = tie.tie_feature_collection(fp)
    # Filter required feature into new collection
    for f in feat_coll['features']:
        print(f['properties']['name'])
    feats = filter(lambda f: f['properties']['name'] == receptor_name,
                  feat_coll['features'])

    new_coll = geojson.FeatureCollection(feats)
#    print(new_coll)
    print('Writing to {}'.format(out_fp))
    s = geojson.dumps(new_coll)
    print(s)
    with open(out_fp, 'w') as sink:
        sink.write(s)
#        sink.write(geojson.dumps(new_coll, sort_keys=True))

### Tests

if __name__ == "__main__":
    args = {
    '--input': None,
     '--output': 'name.geojson',
     '<name>': 'beagle',
     '<nc_dir>': None,
     '<receptor>': None,
     '<tie>': '.\\j0285_receptors.tie',
     'define': True,
     'max_conc': False,
     'max_vol': False,
     'min_time': False,
     'out_fp': 'beagle.geojson',
     'receptor': True,
     'select': False,
     'tie_fp': 'J:\\data\\pp0229\\j0285_receptors.tie'
    }
    define_receptor_cmd(args)

    print("Done __main__")
