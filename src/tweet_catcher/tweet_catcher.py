import os
import time
import pandas as pd
import twint
import logging
import datetime

from .tweet_utils import logger, set_logging_verbosity, make_dir


def twint_search(search=None, user=None, since=None, until=None, output=None):

    c = twint.Config()

    if search is not None:
        c.Search = search

    if user is not None:
        c.Username = user

    # c.Limit = 10

    if since is not None:
        c.Since = since

    if until is not None:
        c.Until = until

    c.Hide_output = True
    # c.Debug = True

    if output is not None:
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
    search=None,
    user=None,
    since=datetime.datetime(1970, 1, 1).isoformat(sep="T", timespec="minutes"),
    until=datetime.datetime.now().isoformat(sep="T", timespec="minutes"),
    directory=os.getcwd(),
    freq_in_str="1D",
    freq_in_timedelta=datetime.timedelta(days=1),
    sleep=10,
    verbose=0,
):
    def twint_call(search, user, since, until, directory, file_name):
        file_name = file_name.replace(" ", "_")
        # path to file
        output = os.path.join(directory, file_name)
        logger.info(f"file: {output}")
        # download tweets
        logger.info(f"download tweet")
        for i in range(8):  # repeat command
            try:
                twint_search(search, user, since, until, output)
            except:
                logger.info("something went wrong. repeat command")
                if sleep:
                    time.sleep(sleep)
                continue
            else:
                logger.info("well done!")
                break

    if search is None and user is None:
        raise ValueError(f"search and user arguments can not be both None")

    set_logging_verbosity(verbose)

    make_dir(directory)

    if freq_in_str is None:
        file_name = f"{search}.csv"
        twint_call(
            search,
            user,
            since.strftime("%Y-%m-%d %H:%M:%S"),
            until.strftime("%Y-%m-%d %H:%M:%S"),
            directory,
            file_name,
        )
        return

    daterange = pd.date_range(since, until, freq=freq_in_str)
    logger.info(f"data range: {daterange}")

    file_basename = user if search is None else search

    for start_date in daterange:

        # define data range
        since = start_date.strftime("%Y-%m-%d %H:%M:%S")
        until = (start_date + freq_in_timedelta).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"data range: {since} {until}")

        # file name
        file_name = f"{file_basename}_{since}.csv"

        # download tweets
        twint_call(search, user, since, until, directory, file_name)

        # wait
        if sleep:
            logger.info(f"waiting for {sleep} sec")
        time.sleep(sleep)
