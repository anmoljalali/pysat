# -*- coding: utf-8 -*-

"""Supports the Ion Velocity Meter (IVM)
onboard the Ionospheric Connections (ICON) Explorer.

Parameters
----------
platform : string
    'icon'
name : string
    'ivm'
tag : string
    None supported
sat_id : string
    'a' or 'b'

Warnings
--------
- No download routine as ICON has not yet been launched
- Data not yet publicly available

Example
-------
    import pysat
    ivm = pysat.Instrument('icon', 'ivm', sat_id='a', tag='level_2',
                           clean_level='clean')
    ivm.download(pysat.datetime(2019, 1, 30), pysat.datetime(2019, 12, 31))
    ivm.load(2017,363)

Author
------
R. A. Stoneback

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
name = 'ivm'
tags = {'level_2': 'Level 2 public geophysical data'}
# dictionary of sat_ids ad tags supported by each
sat_ids = {'a': ['level_2'],
           'b': ['level_2']}
_test_dates = {'a': {'level_2': pysat.datetime(2020, 1, 1)},
               'b': {'level_2': pysat.datetime(2020, 1, 1)}}

fname_a = ''.join(['ICON_L2-7_IVM-A_{year:4d}-{month:02d}-{day:02d}'
                   '_v{version:02d}r{revision:03d}.NC'])
fname_b = ''.join(['ICON_L2-7_IVM-B_{year:4d}-{month:02d}-{day:02d}'
                   '_v{version:02d}r{revision:03d}.NC'])
supported_tags = {'a': {'level_2': fname_a},
                  'b': {'level_2': fname_b}}
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


def default(inst):
    """Default routine to be applied when loading data.

    Parameters
    -----------
    inst : (pysat.Instrument)
        Instrument class object

    Note
    ----
        Removes ICON preamble on variable names.

    """

    remove_icon_names(inst)


def load(fnames, tag=None, sat_id=None):
    """Loads ICON IVM data using pysat into pandas.

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
        inst = pysat.Instrument('icon', 'ivm', sat_id='a', tag='level_2')
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
    """Will download data for ICON IVM, after successful launch and operations.

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
        warnings.warn("Cleaning actions for ICON IVM are not yet defined.")
    return


def remove_icon_names(inst, target=None):
    """Removes leading text on ICON project variable names

    Parameters
    ----------
    inst : pysat.Instrument
        ICON associated pysat.Instrument object
    target : str
        Leading string to remove. If none supplied,
        ICON project standards are used to identify and remove
        leading text

    Returns
    -------
    None
        Modifies Instrument object in place


    """

    if target is None:
        lev = inst.tag
        if lev == 'level_2':
            lev = 'L27'
        elif lev == 'level_0':
            lev = 'L0'
        elif lev == 'level_0p':
            lev = 'L0P'
        elif lev == 'level_1.5':
            lev = 'L1-5'
        elif lev == 'level_1':
            lev = 'L1'
        else:
            raise ValueError('Unknown ICON data level')

        prepend_str = '_'.join(('ICON', lev)) + '_'
    else:
        prepend_str = target

    inst.data.rename(columns=lambda x: x.split(prepend_str)[-1], inplace=True)
    inst.meta.data.rename(index=lambda x: x.split(prepend_str)[-1],
                          inplace=True)
    orig_keys = inst.meta.keys_nD()
    for keynd in orig_keys:
        new_key = keynd.split(prepend_str)[-1]
        new_meta = inst.meta.pop(keynd)
        new_meta.data.rename(index=lambda x: x.split(prepend_str)[-1],
                             inplace=True)
        inst.meta[new_key] = new_meta

    return
