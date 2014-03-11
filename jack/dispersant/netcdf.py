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
def bounds_mask(nc_fp, polygon):
    """
    Find the lat, lon coords that represent the bounds of the polygon

    Args:
        nc_fp: string representing the path to nc file
        polygon: A shapely polygon representing the receptor
    """
    with Dataset(nc_fp) as root:
        lon = root.variables['lon'][:]
        lat = root.variables['lat'][:]
    (minx, miny, maxx, maxy) = polygon.bounds
    # Prepare the mask for the polygon bounds
    lat_mask = np.logical_and(lat > miny, lat < maxy)
    lon_mask = np.logical_and(lon > minx, lon < maxx)

    if __debug__:
        debug('Polygon bounds are: {}'.format(polygon.bounds))
        debug('Shape of lat mask is {}'.format(lat_mask.shape))
        debug('Shape of lon mask is {}'.format(lon_mask.shape))
    return lat, lat_mask, lon, lon_mask

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
    debug (coll)
    # There seems to be an extra layer of lists nesting here!!
    feat = coll['features'][0]
#    print(feat['geometry'])
    poly = asShape(feat['geometry'])
    return poly

def mask_nc_data(nc_fp, nc_var, lat_mask, lon_mask):
    """
    Return the data within the bounds of the receptor polygon
    """
    with Dataset(nc_fp) as root:
        data = root.variables[nc_var]
        arr = data[lat_mask, lon_mask]
    return arr

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

    # Get the bounds and prepare for point in polygon
    polygon = receptor_polygon(receptor_fp)
    lat, lat_mask, lon, lon_mask = bounds_mask(first_nc_fp, polygon)
    prep_poly = prep(polygon)
    lats = lat[lat_mask]
    lons = lon[lon_mask]
    # Filter the points that sre inside the polygon
    points = ( Point(x, y) for x in lon[lon_mask] for y in lat[lat_mask] )
    inside_points = filter(prep_poly.contains, points)
    inside_set    = set( (p.x, p.y) for p in inside_points )

    nc_var = 'conc_max'
    runs_max = []
    for nc_fp in nc_fps:
        arr = mask_nc_data(nc_fp, nc_var, lat_mask, lon_mask)
        shore_concs = np.array([arr[j, i]  for j, lat_v in enumerate(lats)
                                  for i, lon_v in enumerate(lons)
                                  if (lon_v, lat_v) in inside_set])
        max_conc = np.nanmax(shore_concs)
        runs_max.append({'fp': nc_fp, 'max_conc': max_conc})
    map(print, runs_max)
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


def select_min_time_cmd(args):
    pass

def select_max_vol_cmd(args):
    nc_dir = args['<nc_dir>']
    receptor_fp = args['<receptor>']
    assert osp.isdir(nc_dir)
    assert osp.isfile(receptor_fp)

    patt = "J0285_D5_IFO-180_WET_???_SHTS.nc"
    nc_fps = netcdf_files(nc_dir, patt)
    first_nc_fp = nc_fps[0]

    polygon = receptor_polygon(receptor_fp)
    lat, lat_mask, lon, lon_mask = bounds_mask(first_nc_fp, polygon)
    prep_poly = prep(polygon)
    lats = lat[lat_mask]
    lons = lon[lon_mask]
    # Filter the points that sre inside the polygon
    points = ( Point(x, y) for x in lon[lon_mask] for y in lat[lat_mask] )
    inside_points = filter(prep_poly.contains, points)
    inside_set    = set( (p.x, p.y) for p in inside_points )

    nc_var = 'shore_conc'
    runs_max = []
    for nc_fp in nc_fps:
        with Dataset(nc_fp) as root:
            data = root.variables[nc_var]
            arr = data[lat_mask, lon_mask,:]

        shore_concs = np.array([arr[j, i]  for j, lat_v in enumerate(lats)
                                  for i, lon_v in enumerate(lons)
                                  if (lon_v, lat_v) in inside_set])
        max_conc = np.nanmax(shore_concs)
        runs_max.append({'fp': nc_fp, 'max_conc': max_conc})
#    map(print, runs_max)
    plus_concs = filter(lambda d: d['max_conc'] > 0, runs_max)
    ranked_concs = sorted(plus_concs, key=lambda d: d['max_conc'], reverse=True)
    map(print, ranked_concs)

def show(arr):
    plt.imshow(arr, origin='lower', interpolation='nearest')
    plt.show()

    ### Tests

if __name__ == "__main__":

    args = {
        '<nc_dir>': r'J:\data\pp0229\netcdf',
        '<receptor>': r'J:\data\pp0229\vernon.geojson',
    }
    select_max_vol_cmd(args)
    print("Done __main__")
