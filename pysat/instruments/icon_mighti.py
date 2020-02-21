# -*- coding: utf-8 -*-
"""Supports the Michelson Interferometer for Global High-resolution
Thermospheric Imaging (MIGHTI) instrument onboard the Ionospheric
CONnection Explorer (ICON) satellite.  Accesses local data in
netCDF format.

Parameters
----------
platform : string
    'icon'
name : string
    'mighti'
tag : string
    'level_2'
sat_id : string
    'a', 'b', 'red', or 'green'

Warnings
--------
- The cleaning parameters for the instrument are still under development.
- Only supports level-2 data.

Example
-------
    import pysat
    mighti = pysat.Instrument('icon', 'mighti', clean_level='clean')
    mighti.download(pysat.datetime(2019, 1, 30), pysat.datetime(2019, 12, 31))
    mighti.load(2017,363)

Authors
---------
Originated from EUV support.
Jeff Klenzing, Mar 17, 2018, Goddard Space Flight Center
Russell Stoneback, Mar 23, 2018, University of Texas at Dallas
Conversion to MIGHTI, Oct 8th, 2028, University of Texas at Dallas

"""

from __future__ import print_function
from __future__ import absolute_import

import functools
import warnings

import pysat
from pysat.instruments.methods import nasa_cdaweb as cdw

import logging
logger = logging.getLogger(__name__)


platform = 'icon'
name = 'mighti'
tags = {'level_2': 'Level 2 public geophysical data'}
sat_ids = {'a': ['Level_2 MIGHTI A temperature profiles'],
           'b': ['Level_2 MIGHTI B temperature profiles'],
           'green': ['level_2 Green Line Vector Winds'],
           'red': ['Level_2 Red Line Vector Winds']
           }
_test_dates = {'a': {'level_2': pysat.datetime(2019, 12, 25)},
               'b': {'level_2': pysat.datetime(2019, 12, 25)},
               'green': {'level_2': pysat.datetime(2019, 12, 25)},
               'red': {'level_2': pysat.datetime(2019, 12, 25)}}

fname_a = ''.join(['ICON_L2-3_MIGHTI-A_Temperature_{year:4d}-{month:02d}'
                   '-{day:02d}_v{version:02d}r{revision:03d}.NC'])
fname_b = ''.join(['ICON_L2-3_MIGHTI-B_Temperature_{year:4d}-{month:02d}'
                   '-{day:02d}_v{version:02d}r{revision:03d}.NC'])
fname_green = ''.join(['ICON_L2-2_MIGHTI_Vector-Wind-Green_{year:4d}'
                       '-{month:02d}-{day:02d}_v{version:02d}',
                       'r{revision:03d}.NC'])
fname_red = ''.join(['ICON_L2-2_MIGHTI_Vector-Wind-Red_{year:4d}-{month:02d}'
                     '-{day:02d}_v{version:02d}r{revision:03d}.NC'])
supported_tags = {'a': {'level_2': fname_a},
                  'b': {'level_2': fname_b},
                  'green': {'level_2': fname_green},
                  'red': {'level_2': fname_red}}
list_files = functools.partial(cdw.list_files,
                               supported_tags=supported_tags)


def init(self):
    """Initializes the Instrument object with instrument specific values.

    Runs once upon instantiation.

    Parameters
    -----------
    inst : (pysat.Instrument)
        Instrument class object

    Returns
    --------
    Void : (NoneType)
        modified in-place, as desired.

    """

    logger.info("Mission acknowledgements and data restrictions will be " +
                "printed here when available.")

    pass


def clean(inst, clean_level=None):
    """Provides data cleaning based upon clean_level.

    clean_level is set upon Instrument instantiation to
    one of the following:

    'Clean'
    'Dusty'
    'Dirty'
    'None'

    Routine is called by pysat, and not by the end user directly.

    Parameters
    -----------
    inst : (pysat.Instrument)
        Instrument class object, whose attribute clean_level is used to return
        the desired level of data selectivity.

    Returns
    --------
    Void : (NoneType)
        data in inst is modified in-place.

    Note
    ----
        Supports 'clean', 'dusty', 'dirty', 'none'

    """

    if clean_level != 'none':
        logger.info("Cleaning actions for ICON MIGHTI aren't yet defined.")

    return


def default(inst):
    """Default routine to be applied when loading data.

    Note
    ----
        Removes ICON preamble on variable names.

    """
    import pysat.instruments.icon_ivm as icivm
    inst.tag = 'level_2'
    icivm.remove_icon_names(inst, target='ICON_L2_MIGHTI_')


def load(fnames, tag=None, sat_id=None):
    """Loads ICON FUV data using pysat into pandas.

    This routine is called as needed by pysat. It is not intended
    for direct user interaction.

    Parameters
    ----------
    fnames : array-like
        iterable of filename strings, full path, to data files to be loaded.
        This input is nominally provided by pysat itself.
    tag : string
        tag name used to identify particular data set to be loaded.
        This input is nominally provided by pysat itself.
    sat_id : string
        Satellite ID used to identify particular data set to be loaded.
        This input is nominally provided by pysat itself.
    **kwargs : extra keywords
        Passthrough for additional keyword arguments specified when
        instantiating an Instrument object. These additional keywords
        are passed through to this routine by pysat.

    Returns
    -------
    data, metadata
        Data and Metadata are formatted for pysat. Data is a pandas
        DataFrame while metadata is a pysat.Meta instance.

    Note
    ----
    Any additional keyword arguments passed to pysat.Instrument
    upon instantiation are passed along to this routine.

    Examples
    --------
    ::
        inst = pysat.Instrument('icon', 'fuv')
        inst.load(2019,1)

    """

    return pysat.utils.load_netcdf4(fnames, epoch_name='Epoch',
                                    units_label='Units',
                                    name_label='Long_Name',
                                    notes_label='Var_Notes',
                                    desc_label='CatDesc',
                                    plot_label='FieldNam',
                                    axis_label='LablAxis',
                                    scale_label='ScaleTyp',
                                    min_label='ValidMin',
                                    max_label='ValidMax',
                                    fill_label='FillVal')


def download(date_array, tag, sat_id, data_path=None, user=None,
             password=None):
    """Will download data for ICON MIGHTI, after successful launch and
    operations.

    Parameters
    ----------
    date_array : array-like
        list of datetimes to download data for. The sequence of dates need not
        be contiguous.
    tag : string ('')
        Tag identifier used for particular dataset. This input is provided by
        pysat.
    sat_id : string  ('')
        Satellite ID string identifier used for particular dataset. This input
        is provided by pysat.
    data_path : string (None)
        Path to directory to download data to.
    user : string (None)
        User string input used for download. Provided by user and passed via
        pysat. If an account is required for dowloads this routine here must
        error if user not supplied.
    password : string (None)
        Password for data download.
    **kwargs : dict
        Additional keywords supplied by user when invoking the download
        routine attached to a pysat.Instrument object are passed to this
        routine via kwargs.

    Returns
    --------
    Void : (NoneType)
        Downloads data to disk.


    """

    warnings.warn("Downloads aren't yet available.")

    return
