## Author: Rittha
import pandas as pd
import glob
import datetime
import numpy as np
allFiles = glob.glob("Events/*.csv")

frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_)
    list_.append(df)
frame = pd.concat(list_)

frame = frame.drop('Unnamed: 0', axis=1)
frame = frame.reset_index().drop('index', axis=1)

frame['fromto'] = frame[['from','to']].apply(lambda x: '-'.join(x), axis=1)

def short_month(shortMonth):
    return{
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9,
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
    }[shortMonth]


def long_format_parse(f):
    # parse from
    f = f.replace(',','')
    dtl = filter(None, f.split(' '))

    year = int(dtl[3])
    month = short_month(dtl[1])
    day = int(dtl[2])
    day_night = 0
    if dtl[-1].upper() == 'P' or dtl[-1].upper() == ' P':
        day_night = 1

    hour = 0
    minute = 0

    try:
        times = dtl[4][0:-1].split(':')
        hour = int(times[0]) + (12 * day_night)
        minute = int(times[1])
    except:
        pass

    x = datetime.datetime(year,month,day,hour,minute)
    return x

def short_format_parse(f, year, month, day):
    day_night = 0
    if f[-1].upper() == 'P' or f[-1].upper() == ' P':
        day_night = 1

    times = f[0:-1].split(':')
    hour , minute = 0 , 0
    add_day = False

    if len(times) == 2:
        hour = int(times[0]) + (12 * day_night)
        if hour >= 24:
            hour = hour % 24
            add_day = True
        minute = int(times[1])

    elif len(times) == 1:
        hour = int(times[0]) + (12 * day_night)

    x = datetime.datetime(year,month,day,hour,minute)
    if add_day:
        x = x + datetime.timedelta(days=1)
    return x

def custom_parse_dates(dt):
    dt_r = dt.split('-')
    f = dt_r[0]
    t = dt_r[1]
    from_datetime = long_format_parse(f)
    to_datetime = ''
    if len(t) > 10:
        to_datetime = long_format_parse(t)
    else:
        to_datetime = short_format_parse(t, from_datetime.year, from_datetime.month, from_datetime.day)

    duration = to_datetime - from_datetime

    return (from_datetime, to_datetime, duration)


frame = pd.concat([frame, frame['fromto'].apply(lambda x: pd.Series(custom_parse_dates(x)))],axis = 1)
frame = frame.drop(['from','to','fromto'], axis = 1)
frame.columns = [u'event', u'location', u'admision', u'address', u'category', u'from', u'to', u'duration']
frame = frame.sort('from')

frame = frame.drop_duplicates()
frame = frame.reset_index().drop('index',axis=1)
#unique category
tranpose = frame['category'].apply(lambda x: pd.Series([i for i in reversed(str(x).split(','))]))
category_list = np.unique(tranpose)

category_list = category_list[1:].tolist() #remove nan

def categorize(category_data):
    result = np.zeros(len(category_list))
    if isinstance(category_data, basestring):
        cal_list = filter(None, category_data.split(','))
        for cal in cal_list:
            result[category_list.index(cal)] = 1
    return pd.Series(result)

frame = pd.concat([frame, frame['category'].apply(lambda x: categorize(x))], axis=1)
new_col = frame.columns[0:8].tolist()
new_col = new_col + map(str.strip,category_list)
frame.columns = new_col
frame.to_csv('Events/boston_events.csv')
