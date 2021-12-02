from datetime import datetime


def convert_str_to_milliseconds(date_string, date_format="%Y-%m-%d %H:%M:%S.%f"):
    some_date = datetime.strptime(date_string, date_format)
    milliseconds = some_date.timestamp() * 1000
    return milliseconds

