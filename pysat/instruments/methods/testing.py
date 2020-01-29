import os
import numpy as np
import pandas as pds
import pysat


def generate_fake_data(t0, num_array, period=5820, data_range=[0.0, 24.0],
                       cyclic=True):
    """Generates fake data over a given range

    Parameters
    ----------
    t0 : float
        Start time in seconds
    num_array : array_like
        Array of time steps from t0.  This is the index of the fake data
    period : int
        The number of seconds per period.
        (default = 5820)
    data_range : float
        For cyclic functions, the range of data values cycled over one period.
        Not used for non-cyclic functions.
        (default = 24.0)
    cyclic : bool
    """

    if cyclic:
        uts_root = np.mod(t0, period)
        data = (np.mod(uts_root + num_array, period)
                * (np.diff(data_range)[0] / float(period))) + data_range[0]
    else:
        data = ((t0 + num_array) / period).astype(int)

    return data


def generate_times(fnames, sat_id, freq='1S'):
    """Construct list of times for simulated instruments

    Parameters
    ----------
    fnames : (list)
        List of filenames
    sat_id : (str or NoneType)
        Instrument satellite ID (accepts '' or a number (i.e., '10'), which
        specifies the number of data points to include in the test instrument)
    freq : string
        Frequency of temporal output, compatible with pandas.date_range
        [default : '1S']

    Outputs
    -------
    uts : (array)
        Array of integers representing uts for a given day
    index : (DatetimeIndex)
        The DatetimeIndex to be used in the pysta test instrument objects
    date : (datetime)
        The requested date reconstructed from the fake file name
    """

    # grab date from filename
    parts = os.path.split(fnames[0])[-1].split('-')
    yr = int(parts[0])
    month = int(parts[1])
    day = int(parts[2][0:2])
    date = pysat.datetime(yr, month, day)

    # Create one day of data at desired frequency
    index = pds.date_range(start=date, end=date+pds.DateOffset(seconds=86399),
                           freq=freq)
    # Allow numeric string to select first set of data
    if sat_id.isnumeric() and (int(sat_id) < 86400):
        index = index[0:int(sat_id)]

    uts = index.hour*3600 + index.minute*60 + index.second

    return uts, index, date
