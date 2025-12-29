from datetime import datetime, timedelta
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def timeparse(str):
    # make an arr of [date, [start, end]]
    shiftarr = str.split(' ')
    shiftarr[1] = shiftarr[1].split('-')
    
    # convert the date to datetime
    day_index = days.index(shiftarr[0])
    days_ahead = day_index - datetime.today().weekday()
    if days_ahead <= 0:
        days_ahead += 7
    shift_date = (datetime.today() + timedelta(days=days_ahead)).date()
    
    # convert the times to datetime and combine date & times
    start = datetime.combine(shift_date, datetime.strptime(shiftarr[1][0], "%I%p").time())
    end = datetime.combine(shift_date, datetime.strptime(shiftarr[1][1], "%I%p").time())
    end = end + timedelta(days=1) if shiftarr[1][1] == "12am" else end
    
    return (start, end)
