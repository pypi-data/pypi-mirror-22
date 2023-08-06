from __future__ import division
from datetime import timedelta,datetime, time
from pytz import UTC
import numpy as np
from dateutil.parser import parse
from xarray import DataArray
#
from matplotlib.dates import DateFormatter
from matplotlib.dates import MinuteLocator,SecondLocator

def datetime2yd(T):
    """
    Inputs:
    T: Numpy 1-D array of datetime.datetime OR string suitable for dateutil.parser.parse

    Outputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER)
    utsec: seconds from midnight utc
    """
    T = forceutc(T)
    T = np.atleast_1d(T)

    utsec= np.empty_like(T, float)
    yd =   np.empty_like(T, int)
    for i,t in enumerate(T):
        utsec[i] = dt2utsec(t)
        yd[i] = t.year*1000 + int(t.strftime('%j'))

    return yd.squeeze()[()] , utsec.squeeze()[()]

def yd2datetime(yd,utsec=None):
    """
    Inputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER 7 digits)

    outputs:
    t: datetime

    http://stackoverflow.com/questions/2427555/python-question-year-and-day-of-year-to-date
    """
    yd = str(yd)
    assert len(yd)==7,'yyyyddd expected'

    year = int(yd[:4])
    assert 0 < year < 3000,'year not in expected format'

    dt = forceutc(datetime(year, 1, 1) + timedelta(days=int(yd[4:]) - 1))
    if utsec is not None:
        dt += timedelta(seconds=utsec)

    return dt


def datetime2gtd(T, glon=np.nan):
    """
    Inputs:
    T: Numpy 1-D array of datetime.datetime OR string suitable for dateutil.parser.parse
    glon: Numpy 2-D array of geodetic longitudes (degrees)

    Outputs:
    iyd: day of year
    utsec: seconds from midnight utc
    stl: local solar time
    """
    T =   np.atleast_1d(T)
    glon= np.atleast_2d(glon)
    iyd=  np.empty_like(T, int)
    utsec=np.empty_like(T, float)
    stl = np.empty((T.size, glon.shape[0], glon.shape[1]))

    for i,t in enumerate(T):
        t = forceutc(t)
        iyd[i] = int(t.strftime('%j'))
        #seconds since utc midnight
        utsec[i] = dt2utsec(t)

        stl[i,...] = utsec[i]/3600 + glon/15 #FIXME let's be sure this is appropriate

    return iyd,utsec,stl

#def dt2utsec(t: datetime) -> float:
def dt2utsec(t):
    """
    input: datetime
    output: float utc seconds since THIS DAY'S MIDNIGHT
    """
    t = forceutc(t)

    return timedelta.total_seconds(t-datetime.combine(t.date(),time(0,tzinfo=UTC)))


def forceutc(t):
    """
    Add UTC to datetime-naive and convert to UTC for datetime aware

    input: python datetime (naive, utc, non-utc) or Numpy datetime64  #FIXME add Pandas and AstroPy time classes
    output: utc datetime
    """
#%% polymorph to datetime
    if isinstance(t,str):
        t = parse(t)
    elif isinstance(t, np.datetime64):
        t=t.astype('M8[ms]').astype('O') #for Numpy 1.10 at least...
    elif isinstance(t,datetime):
        pass
    elif isinstance(t,(np.ndarray,list,tuple)):
        return np.asarray([forceutc(T) for T in t])
    else:
        raise TypeError('datetime only input')
#%% enforce UTC on datetime
    if t.tzinfo == None: #datetime-naive
        t = t.replace(tzinfo = UTC)
    else: #datetime-aware
        t = t.astimezone(UTC) #changes timezone, preserving absolute time. E.g. noon EST = 5PM UTC
    return t


"""
http://stackoverflow.com/questions/19305991/convert-fractional-years-to-a-real-date-in-python
Authored by "unutbu" http://stackoverflow.com/users/190597/unutbu

In Python, go from decimal year (YYYY.YYY) to datetime,
and from datetime to decimal year.
"""
def yeardec2datetime(atime):
    """
    Convert atime (a float) to DT.datetime
    This is the inverse of datetime2yeardec.
    assert dt2t(t2dt(atime)) == atime
    """
    if isinstance(atime,(float,int)): #typically a float

        year = int(atime)
        remainder = atime - year
        boy = datetime(year, 1, 1)
        eoy = datetime(year + 1, 1, 1)
        seconds = remainder * (eoy - boy).total_seconds()

        return forceutc(boy + timedelta(seconds=seconds))
    elif isinstance(atime[0],float):
        T = []
        for t in atime:
            T.append(yeardec2datetime(t))
        return T
    else:
        raise TypeError('expecting float, not {}'.format(type(atime)))

def datetime2yeardec(t):
    """
    Convert a datetime into a float. The integer part of the float should
    represent the year.
    Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
    time distances should be preserved: If bdate-adate=ddate-cdate then
    dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
    """
    if isinstance(t,str):
        t = parse(t)

    t = forceutc(t)

    assert isinstance(t,datetime)

    year = t.year
    boy = datetime(year, 1, 1,tzinfo=UTC)
    eoy = datetime(year + 1, 1, 1, tzinfo=UTC)
    return year + ((t - boy).total_seconds() / ((eoy - boy).total_seconds()))


#%%
def find_nearest(x,x0):
    """
    This find_nearest function does NOT assume sorted input

    inputs:
    x: array (float, int, datetime, h5py.Dataset) within which to search for x0
    x0: singleton or array of values to search for in x

    outputs:
    idx: index of flattened x nearest to x0  (i.e. works with higher than 1-D arrays also)
    xidx: x[idx]

    Observe how bisect.bisect() gives the incorrect result!

    idea based on:
    http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

    """
    x =  np.asanyarray(x) #for indexing upon return
    x0 = np.atleast_1d(x0)
#%%
    if x.size==0 or x0.size==0:
        raise ValueError('empty input(s)')

    assert x0.ndim in (0,1),'2-D x0 not handled yet'
#%%
    ind = np.empty_like(x0,dtype=int)

    # NOTE: not trapping IndexError (all-nan) becaues returning None can surprise with slice indexing
    for i,xi in enumerate(x0):
        if xi is not None and (isinstance(xi,datetime) or np.isfinite(xi)):
            ind[i] = np.nanargmin(abs(x-xi))
        else:
            raise ValueError('x0 must NOT be None or NaN to avoid surprising None return value')

    return ind.squeeze()[()], x[ind].squeeze()[()]   # [()] to pop scalar from 0d array while being OK with ndim>0

def INCORRECTRESULT_using_bisect(x,X0): #pragma: no cover
    X0 = np.atleast_1d(X0)
    x.sort()
    ind = [bisect(x,x0) for x0 in X0]

    x = np.asanyarray(x)
    return np.asanyarray(ind),x[ind]

if __name__ == '__main__':
    from bisect import bisect

    print(find_nearest([10,15,12,20,14,33],[32,12.01]))

    print(INCORRECTRESULT_using_bisect([10,15,12,20,14,33],[32,12.01]))
#%%

def tickfix(t,fg,ax,tfmt='%H:%M:%S'):
    majtick,mintick = timeticks(t[-1] - t[0])
    if majtick:
        ax.xaxis.set_major_locator(majtick)
    if mintick:
        ax.xaxis.set_minor_locator(mintick)
    ax.xaxis.set_major_formatter(DateFormatter(tfmt))
    fg.autofmt_xdate()

    ax.autoscale(True,'x',tight=True)

 #   ax.tick_params(axis='both',which='both')
   # ax.grid(True,which='both')

def timeticks(tdiff):
    """
    NOTE do NOT use "interval" or ticks are misaligned!  use "bysecond" only!
    """
    if isinstance(tdiff,DataArray): #len==1
        tdiff = timedelta(microseconds=tdiff.item()/1e3)

    assert isinstance(tdiff,timedelta),'expecting datetime.timedelta'

    if tdiff > timedelta(hours=2):
        return None,None

    elif tdiff > timedelta(minutes=20):
        return MinuteLocator(byminute=range(0,60,5)),  MinuteLocator(byminute=range(0,60,2))

    elif (timedelta(minutes=10) < tdiff) & (tdiff<=timedelta(minutes=20)):
        return MinuteLocator(byminute=range(0,60,2)),  MinuteLocator(byminute=range(0,60,1))

    elif (timedelta(minutes=5) < tdiff) & (tdiff<=timedelta(minutes=10)):
        return MinuteLocator(byminute=range(0,60,1)),  SecondLocator(bysecond=range(0,60,30))

    elif (timedelta(minutes=1) < tdiff) & (tdiff<=timedelta(minutes=5)):
        return SecondLocator(bysecond=range(0,60,30)), SecondLocator(bysecond=range(0,60,10))

    elif (timedelta(seconds=30) < tdiff) &(tdiff<=timedelta(minutes=1)):
        return SecondLocator(bysecond=range(0,60,10)),  SecondLocator(bysecond=range(0,60,2))

    else:
        return SecondLocator(bysecond=range(0,60,2)),  SecondLocator(bysecond=range(0,60,1))
