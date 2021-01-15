from datetime import datetime, timedelta

from dateutil import parser as dateutil_parser

from .messages import LEMBRETE


def prettify_date(dt_object):
    """
    Pretty-format a datetime object

    Args:
        dt_object(datetime.datetime): A datetime object.

    Returns:
        str: A pretty-formatted date.
    """

    return dt_object.strftime("%A %Hh%M, %d %b %Y")


def parse_date(date_args):
    """
    Parse argument into a datetime object

    Args:
        date_args: A list or datetime object to be parsed.

    Returns:
        tuple: A tuple of a string-date and a datetime object.
    """

    if isinstance(date_args, (list, tuple)):
        date_args = " ".join(date_args)
    elif isinstance(date_args, datetime):
        date_args = str(date_args)
    datetime_obj = dateutil_parser.parse(date_args)
    parsed_date = prettify_date(datetime_obj)
    return parsed_date, datetime_obj


def get_meeting_range(date_args):
    """
    Parse argument into datetimes and datetime range.

    Args:
        date_args: A list or datetime object to be parsed.

    Returns:
        tuple: A tuple of a string-date, a datetime object and
        a list of tuple representing the next meetings.
    """

    # Get message meeting and following ones
    parsed_date, datetime_obj = parse_date(date_args)
    next_meetings, interval = [
        (parsed_date, datetime_obj),
    ], 7
    for _ in range(3):
        next_meetings.append(parse_date(datetime_obj + timedelta(days=interval)))
        interval += interval

    return parsed_date, datetime_obj, next_meetings


def add_timedeltas(dt_object):
    """
    Localize and buffer meeting datetime object

    Adds a timedelta of +3 to localize to GMT-3 and
    a timedelta of -30min for the reminder.

    Args:
        dt_object(datetime.datetime): A datetime object.

    Returns:
        datetime.datetime: A datetime object localized and buffered.
    """

    return dt_object + timedelta(hours=3) - timedelta(minutes=30)


def generate_reminders(next_meetings):
    """
    Generate list of datetimes for the alarms

    Args:
        next_meetings(list): The list made by get_meeting_range.

    Returns:
        list: A list of datetime objects corresponding to alarm times.
    """
    alarm_times = [add_timedeltas(meeting[1]) for meeting in next_meetings]

    return alarm_times


def alarm(context):
    """
    Handle sending the alarm message
    """
    job = context.job
    context.bot.send_message(job.context, text=LEMBRETE)