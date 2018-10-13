import jdatetime


def to_gregorian(strtime):
    """ Get string "1397-07-21 12:32" and return a gregorian datetime. """
    if strtime:
        response = jdatetime.datetime.strptime(
            strtime, "%Y-%m-%d %H:%M").togregorian()
    else:
        response = strtime
    return response


def to_jalali(gr_datetime):
    """ Get a gregorian date time and return a string "1397-07-21 12:32". """

    if gr_datetime:
        response = jdatetime.datetime.fromgregorian(
            datetime=gr_datetime).strftime("%Y-%m-%d %H:%M")
    else:
        response = gr_datetime
    return response
