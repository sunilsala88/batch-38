import datetime

dt1=datetime.datetime(2026, 9, 14, 10, 30, 45)
print(dt1.weekday()) 

import datetime as dt

dt2=dt.datetime(2026, 9, 15, 10, 30, 45)
print(dt2.weekday())

d1=dt.date(2026, 9, 14)
print(d1)

t1=dt.time(10, 30, 45)
print(t1)


#str to datetime
s1='2026-Aug-14 10:30:45'
f1='%Y-%b-%d %H:%M:%S'
dt3=dt.datetime.strptime(s1,f1)
print(dt3)
#int

#dt