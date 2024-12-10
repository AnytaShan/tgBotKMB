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
        match week_day:
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return 4
            case 5 | 6 | 7:
                return 5
    else:
        match week_day:
            case 1:
                return 6
            case 2:
                return 7
            case 3:
                return 8
            case 4:
                return 9
            case 5 | 6 | 7:
                return 10


    

