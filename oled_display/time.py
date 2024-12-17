import datetime

def get_total_time_elapsed() -> datetime.timedelta:
    """
    Calculate the total running time of Longplayer to date.

    This is derived by converting the current time into UTC, and then calculating the
    time elapsed since 2000-01-01 00:00:00 (at the international date line).

    Returns:
        datetime.timedelta: The time delta.
    """
    start_time = datetime.datetime.strptime("2000-01-01T00:00:00+1200", "%Y-%m-%dT%H:%M:%S%z")
    current_time = datetime.datetime.now(datetime.timezone.utc)
    return current_time - start_time

def get_time_elapsed_elements():
    timedelta = get_total_time_elapsed()

    days_per_year = 365.2425
    years = timedelta.days // days_per_year
    days = timedelta.days - (years * days_per_year)
    hours = timedelta.seconds // 3600
    minutes = (timedelta.seconds - hours * 3600) // 60
    seconds = timedelta.seconds % 60
    microseconds = timedelta.microseconds / 1000

    return years, days, hours, minutes, seconds, microseconds
