#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Module: cmd.py
Package:
Created on Sun Mar 09 10:24:14 2014
@author: gav
Description:

Usage:  jack select max_conc (<nc_dir> <receptor> [--output <out>] | --input <in>)
        jack select max_vol  (<nc_dir> <receptor> [--output <out>] | --input <in>)
        jack select min_time (<nc_dir> <receptor> [--output <out>] | --input <in>)
        jack define receptor (<tie> <name>        [--output <out>] | --input <in>)

Options:
    -h --help               Show this screen
    -v --version            Show version
    -i --input <in>         Yaml input file
    -o --output <out>       Filename of output file [default: name.geojson]
"""
### Imports
from __future__ import print_function, division

import os.path as osp
from docopt import docopt
from pprint import pprint, pformat

from jack.dispersant.receptors import define_receptor_cmd
from jack.dispersant.netcdf import select_max_conc_cmd

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
def lookup_function(verb, subject):

    d = {
        ('define', 'receptor'): define_receptor_cmd,
        ('select', 'max_conc'): select_max_conc_cmd,
    }
    return d[(verb, subject)]



def dispatch_keys(args, verbs=None, subjects=None):
    """
    Parse the verb and subject from the args
    """
    verbs = verbs or ('select', 'define')
    subjects = subjects or ('max_conc', 'max_vol', 'min_time', 'max_conc',
                            'receptor')
    vb = next(v for v in verbs if args[v])
    sbj = next(s for s in subjects if args[s])
    return vb, sbj

def cleanup_args(args, key_tup):
    """
    Remove the keys not required for this dispatch func

    Chiefly remove angles and dashes please
    """
    if key_tup == ('define', 'receptor'):
        # Cleanup tie filepath
        tie_fp = osp.abspath(args['<tie>'])
        if osp.isfile(tie_fp):
            args['tie_fp'] = tie_fp
        else:
            err_msg = 'No such file found: {}'.format(tie_fp)
            raise IOError, err_msg
        # Cleanup output file
        if args['--output'] == 'name.geojson':
            args['out_fp'] = args['<name>'] + '.geojson'

    return args

def main(args):
#    verbs = {'select', 'define'}
#    subjects = {'max_conc', 'max_vol', 'min_time', 'max_conc'}

    vb, sbj = dispatch_keys(args)
    dispatch_func = lookup_function(vb, sbj)
    args = cleanup_args(args, (vb, sbj))
    dispatch_func(args)
#    print(vb, sbj)
#    pprint(args)


def cmd():
    args = docopt(__doc__, version="jack v0.1.0")
    main(args)



### Tests

if __name__ == "__main__":

    print("Done __main__")
