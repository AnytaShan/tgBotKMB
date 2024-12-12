import re
import datetime 
from datetime import date

now = str(datetime.datetime.now())
date_now = re.split(":|-| ", now)

year = int(date_now[0])
month = int(date_now[1])
day = int(date_now[2])
hour = int(date_now[3])
minute = int(date_now[4])

week_now = str(date(year, month, day).isocalendar())
list_week = re.findall(r'\d+', week_now)
week = int(list_week[1])
week_day = int(list_week[2])

def get_DayOfTheWeekId():
    if week % 2 == 0:
        return [1, 2, 3, 4, 5][week_day - 1]
    else:
        return [6, 7, 8, 9, 10][week_day - 1]


    

