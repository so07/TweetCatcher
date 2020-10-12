import os
import time
import pandas as pd
import twint
import logging
import datetime

from .tweet_utils import logger, set_logging_verbosity, make_dir


def twint_search(search, since, until, output):

    c = twint.Config()

    c.Search = search
    # c.Username = search

    c.Limit = 10

    c.Since = since
    c.Until = until
    c.Hide_output = True
    # c.Debug = True

    c.Output = output
    c.Store_csv = True

    c.Count = True

    # c.Translate = True
    # c.TranslateDest = "en"

    if since or until:
        print(since, until)

    # c.Resume = 'wm_last.csv'

    twint.run.Search(c)


def extend_search(keys):
    l = []
    for i in keys:
        l.append(i.lower())
        l.append(i.upper())
        l.append(i.capitalize())
    return l


def tweet_catcher(
    search,
    since,
    until,
    directory,
    freq_in_str="1D",
    freq_in_timedelta=datetime.timedelta(days=1),
    sleep=10,
    verbose=0,
):
    def twint_call(search, since, until, directory, file_name):
        file_name = file_name.replace(" ", "_")
        # path to file
        output = os.path.join(directory, file_name)
        logger.info(f"file: {output}")
        # download tweets
        logger.info(f"download tweet")
        twint_search(search, since, until, output)

    set_logging_verbosity(verbose)

    make_dir(directory)

    if freq_in_str is None:
        file_name = f"{search}.csv"
        twint_call(search, None, None, directory, file_name)
        return

    daterange = pd.date_range(since, until, freq=freq_in_str)
    logger.info(f"data range: {daterange}")

    for start_date in daterange:

        # define data range
        since = start_date.strftime("%Y-%m-%d %H:%M:%S")
        until = (start_date + freq_in_timedelta).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"data range: {since} {until}")

        # file name
        file_name = f"{search}_{since}.csv"

        # download tweets
        twint_call(search, since, until, directory, file_name)

        # wait
        if sleep:
            logger.info(f"waiting for {sleep} sec")
        time.sleep(sleep)
