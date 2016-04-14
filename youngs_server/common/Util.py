from datetime import  datetime, time

def dateToString(datetime_str):
    """ dump string of today's datetime to datetime object"""
    try:
        if len(datetime_str) <= 10:
            # cast date to datetime
            result_datetime = datetime.strptime(datetime_str, "%y/%m/%d")
        else:
            result_datetime = datetime.strptime(datetime_str, "%y/%m/%d %h:%m")

            return result_datetime
    except Exception as e:
        print e.message
        return None

def timeToString(time_str):
    """ dump string of today's datetime to datetime object"""
    try:
        return time.strptime(time_str, "%h:%m").time()
    except Exception as e:
        print e.message
        return None