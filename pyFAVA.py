#!/usr/bin/env python
"""
------------------------------------------------------------------------

Script to download FAVA results:

Author: Daniel Kocevski (daniel.kocevski@nasa.gov)
Date: September 25th, 2022

Usage Examples:
import FAVApy
FAVApy.getData(week=1, sigma=6)

------------------------------------------------------------------------
"""

import urllib.request
import json 
import numpy
from astropy import units as u
from astropy.coordinates import SkyCoord


# Define the FAVA url
fava_api_url = 'https://fermi.gsfc.nasa.gov/ssc/data/access/lat/FAVA/queryDB_2FAV.php'

class DataCatalog(dict):
    """
    An dictionary object used to store the FAVA data as numpy array that are accessible through key value pairs

    """ 
    def __init__(self): 
        self['flareID'] = numpy.array([])
        self['num'] = numpy.array([])
        self['best_ra'] = numpy.array([])
        self['best_dec'] = numpy.array([])
        self['best_r95'] = numpy.array([])
        self['bestPositionSource'] = numpy.array([])
        self['fava_ra'] = numpy.array([])
        self['fava_dec'] = numpy.array([])
        self['lbin'] = numpy.array([])
        self['bbin'] = numpy.array([])
        self['gall'] = numpy.array([])
        self['galb'] = numpy.array([])
        self['tmin'] = numpy.array([])
        self['tmax'] = numpy.array([])
        self['sigma'] = numpy.array([])
        self['avnev'] = numpy.array([])
        self['nev'] = numpy.array([])
        self['he_nev'] = numpy.array([])
        self['he_avnev'] = numpy.array([])
        self['he_sigma'] = numpy.array([])
        self['sundist'] = numpy.array([])
        self['varindex'] = numpy.array([])
        self['favasrc'] = numpy.array([])
        self['fglassoc'] = numpy.array([])
        self['assoc'] = numpy.array([])
        self['le_ts'] = numpy.array([])
        self['le_tssigma'] = numpy.array([])
        self['le_ra'] = numpy.array([])
        self['le_dec'] = numpy.array([])
        self['le_gall'] = numpy.array([])
        self['le_galb'] = numpy.array([])
        self['le_r95'] = numpy.array([])
        self['le_contflag'] = numpy.array([])
        self['le_sundist'] = numpy.array([])
        self['le_dist2bb'] = numpy.array([])
        self['le_ffsigma'] = numpy.array([])
        self['le_hightsfrac'] = numpy.array([])
        self['le_gtlts'] = numpy.array([])
        self['le_flux'] = numpy.array([])
        self['le_fuxerr'] = numpy.array([])
        self['le_index'] = numpy.array([])
        self['le_indexerr'] = numpy.array([])
        self['he_ts'] = numpy.array([])
        self['he_tssigma'] = numpy.array([])
        self['he_ra'] = numpy.array([])
        self['he_dec'] = numpy.array([])
        self['he_gall'] = numpy.array([])
        self['he_galb'] = numpy.array([])
        self['he_r95'] = numpy.array([])
        self['he_contflag'] = numpy.array([])
        self['he_sundist'] = numpy.array([])
        self['he_dist2bb'] = numpy.array([])
        self['he_ffsigma'] = numpy.array([])
        self['he_hightsfrac'] = numpy.array([])
        self['he_le_dist'] = numpy.array([])
        self['he_gtlts'] = numpy.array([])
        self['he_flux'] = numpy.array([])
        self['he_fuxerr'] = numpy.array([])
        self['he_index'] = numpy.array([])
        self['he_indexerr'] = numpy.array([])
        self['week'] = numpy.array([])
        self['dateStart'] = numpy.array([])
        self['dateStop'] = numpy.array([])


def getWeeklySources(week=1, threshold=6, dataCatalog=None, verbose=True, test=False):
    """
    Function to download a week's worth of FAVA data.

    Returns a DataCatalog object with data arrays accessible through key value pairs

    """ 

    # Construct the full url
    requested_url = '%s?typeOfRequest=SourceList&week=%s&threshold=%s' % (fava_api_url, week, threshold)

    if verbose == True:
        print(requested_url)

    if test == True:
        return None

    # Request the url. The result should be a json file
    with urllib.request.urlopen(requested_url) as url:

        # Download the json file
        data = json.load(url)

        if dataCatalog is None:

            # Create a new list of sources
            dataCatalog = DataCatalog()

        # Loop through each of the sources in the data dictionary
        for item in data:

            # Loop through each key value pair and add them to the data arrays
            for key in item.keys():
                try:
                    dataCatalog[key] = numpy.append(dataCatalog[key], float(item[key]))
                    float(item[key])
                except:
                    dataCatalog[key] = numpy.append(dataCatalog[key], item[key])

    return dataCatalog


def downloadCatalog(start_week=1, end_week=721, threshold=6, verbose=True, test=False):
    """
    Function to download multiple weeks worth of FAVA data. 

    Returns a DataCatalog object with data arrays accessible through key value pairs

    """ 

    week = start_week
    dataCatalog = None

    print("\nDownloading FAVA data...\n")

    while week < end_week+1:

        # Download the data
        dataCatalog = getWeeklySources(week=week, threshold=threshold, dataCatalog=dataCatalog, verbose=verbose)

        # Increment the week
        week = week + 1

    print('\nDownloaded data for %s sources.\n' % len(dataCatalog['flareID']))

    return dataCatalog


def selectGalacticSources(dataCatalog, dgalb=10, return_index=False):
    """
    Function to produce a subset of galactic sources 

    Returns a DataCatalog object with data arrays accessible through key value pairs

    """ 

    # Define a new data catalog object
    galacticDataCatalog = DataCatalog()

    # Find the sources that are within +/- dgalb
    best_ra = dataCatalog['best_ra']
    best_dec = dataCatalog['best_dec']

    skyCoordinate = SkyCoord(ra=best_ra *u.degree, dec=best_dec *u.degree, frame='fk5')
    best_gall = skyCoordinate.galactic.l.value
    best_galb = skyCoordinate.galactic.b.value

    index = numpy.where((best_galb >= (-1*dgalb)) & (best_galb <= dgalb))

    # Loop through each of the variables in the dataCatalog and select only the galactic sources
    for key in dataCatalog.keys():

        # Fill the new data catalog
        galacticDataCatalog[key] = numpy.append(galacticDataCatalog[key], dataCatalog[key][index])

    print('\nSelected %s sources.\n' % len(galacticDataCatalog['flareID']))

    if return_index == True:
        return index
    else:
        return galacticDataCatalog

