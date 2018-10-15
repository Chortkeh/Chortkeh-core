import jdatetime


def to_gregorian(strtime=None):
    """ Get string "1397-07-21 12:32" and return a gregorian datetime. """
    if strtime:
        response = jdatetime.datetime.strptime(
            strtime, "%Y-%m-%d %H:%M").togregorian()
    else:
        response = strtime
    return response


def to_jalali(gr_datetime=None):
    """ Get a gregorian date time and return a string "1397-07-21 12:32". """

    if gr_datetime:
        response = jdatetime.datetime.fromgregorian(
            datetime=gr_datetime).strftime("%Y-%m-%d %H:%M")
    else:
        response = gr_datetime
    return response


def str_to_jdate(strtime=None):
    """ Get string "1397-07-21 12:32" and return a jdateTime. """
    if strtime:
        response = jdatetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M")
    else:
        response = strtime
    return response


def jdate_to_str(j_datetime=None):
    """ Get a JdateTime and return a string "1397-07-21 12:32". """

    if j_datetime:
        response = j_datetime.strftime("%Y-%m-%d %H:%M")
    else:
        response = j_datetime
    return response
