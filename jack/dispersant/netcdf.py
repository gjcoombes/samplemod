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

import os
import os.path as osp
import fnmatch
from pprint import pprint, pformat

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

import geojson
from netCDF4 import Dataset
from shapely.geometry import Point, MultiPolygon, asShape
from shapely.prepared import prep


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
def netcdf_files(nc_dir, patt=None):
    """
    Return the nc_files amtching the pattern in dir
    """
    patt = patt or "J0285_D5_IFO-180_WET_file_???.nc"
    files = fnmatch.filter(os.listdir(nc_dir), patt)
    filepaths = [osp.join(nc_dir, f) for f in files]
    return filepaths

def receptor_polygon(receptor_fp):
    """
    Convert the geojson into a shapely polygon (or multi)
    """
    with open(receptor_fp) as source:
        coll = geojson.load(source)
    # There seems to be an extra layer of lists nesting here!!
    feat = coll['features'][0][0]
#    print(feat['geometry'])
    poly = asShape(feat['geometry'])
    return poly

def select_max_conc_cmd(args):
    """
    Find the run with the highest surface concentration within the receptor

     we need the 'conc_max' variable
    """
    nc_dir = args['<nc_dir>']
    receptor_fp = args['<receptor>']
    assert osp.isdir(nc_dir)
    assert osp.isfile(receptor_fp)

    # Max conc will be the conc_max var
    nc_fp = r'J:\data\pp0229\netcdf\J0285_D5_IFO-180_WET_file_015.nc'
    patt = 'J0285_D5_IFO-180_WET_file_???.nc'
    nc_fps = [ osp.join(nc_dir, fn)
               for fn in fnmatch.filter(os.listdir(nc_dir), patt) ]

    # Pickup the grid first to make polygon mask
    first_nc_fp = nc_fps[0]
    with Dataset(first_nc_fp) as root:
        lon = root.variables['lon'][:]
        lat = root.variables['lat'][:]
    # Get the bounds and prepare for point in polygon
    poly = receptor_polygon(receptor_fp)
    prep_poly = prep(poly)
    print('Polygon bounds is {}'.format(poly.bounds))
    (minx, miny, maxx, maxy) = poly.bounds
    # Prepare the mask for the polygon bounds
    lat_mask = np.logical_and(lat > miny, lat < maxy)
    lon_mask = np.logical_and(lon > minx, lon < maxx)
    lats = lat[lat_mask]
    lons = lon[lon_mask]
    # Filter the points that sre inside the polygon
    points = ( Point(x, y) for x in lon[lon_mask] for y in lat[lat_mask] )
    inside_points = filter(prep_poly.contains, points)
    inside_set    = set( (p.x, p.y) for p in inside_points )

    runs_max = []
    for nc_fp in nc_fps:
        with Dataset(nc_fp) as root:
            # Should compare grids fr equality here
            surf_max = root.variables['conc_max']
            arr = surf_max[lat_mask, lon_mask]
        surf_concs = ( arr[j, i]  for j, lat_v in enumerate(lats)
                                  for i, lon_v in enumerate(lons)
                                  if (lon_v, lat_v) in inside_set )
        max_conc = max(surf_concs)
        runs_max.append({'fp': nc_fp, 'max_conc': max_conc})

    plus_concs = filter(lambda d: d['max_conc'] > 0, runs_max)
    ranked_concs = sorted(plus_concs, key=lambda d: d['max_conc'], reverse=True)
    map(print, ranked_concs)
#    concs = []
#    for j, lat_v in enumerate(lats):
#        for i, lon_v in enumerate(lons):
#            print(j, i)
#            if (lon_v, lat_v) in inside_set:
#                print('Found conc {}'.format(arr[j, i]))
#                concs.append(arr[j, i])
#    print("Max conc is {}".format(max(concs)))



#    arr = surf_max[i, j]
#    plt.imshow(arr, origin='lower', interpolation='nearest')
#    plt.show()

#    for v in root.variables:
#        print(v)

def select_min_time_cmd(args):
    pass

def select_max_vol_cmd(args):
    pass

### Tests

if __name__ == "__main__":

    args = {
        '<nc_dir>': r'J:\data\pp0229\netcdf',
        '<receptor>': r'J:\data\pp0229\bare.geojson',
    }
    select_max_conc_cmd(args)
    print("Done __main__")
