import os
import glob
import logging
import datetime
import csv
import pandas as pd

logger = logging.getLogger()


def set_logging_verbosity(verbose):
    level = logging.INFO

    if verbose:
        level = logging.DEBUG

    logging.basicConfig(level=level)


def make_dir(directory):
    """make directory if not exists"""
    if not os.path.exists(directory):
        logger.info(f"make dir: {directory}")
        os.makedirs(directory)


def sniff_sep(f):
    """return separator in a csv file"""
    with open(f, "r") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline(), delimiters=",|?;/")
    return dialect.delimiter


def read_csv(path, pattern="*", extension="csv"):
    """read csv file and return pandas dataframe"""

    # file pattern
    file_pattern = "*"
    if pattern:
        file_pattern = pattern
    file_pattern += "." + extension

    logger.debug(f"file patter: {file_pattern}")

    # list of files
    ls = glob.glob(os.path.join(path, file_pattern))

    logger.debug(f"Found {len(ls)} files")
    logger.debug(" ".join(ls))

    # read files

    df = pd.DataFrame()

    for f in ls:
        logger.debug(f"reading file: {f}")

        sep = sniff_sep(f)
        logger.debug(f"csv separator: {sep}")

        d = pd.read_csv(f, sep=sep, dtype=str)
        logger.debug(f"dataframe length: {len(d)}")

        df = pd.concat([df, d])

    # convert date in datetime.date

    # df.date = pd.to_datetime(df.date, format="%Y-%m-%d")
    # df.time = pd.to_datetime(df.time, format="%H:%M:%S")

    logger.info(f"tweets: {len(df)}")

    logger.debug(df.columns)

    return df


def write_df_by_date(df, output, format="csv", sep=","):
    logger.debug("@write_df_by_date")

    if df.empty:
        logger.debug("empty dataframe")
        return

    logger.debug(f"output directory: {output}")
    make_dir(output)

    daterange = pd.date_range(df.date.min(), df.date.max(), freq="1D")

    for i in daterange:
        date = str(i.date())

        logger.debug(f"analize date: {date}")

        # select df by date
        d = df[df.date == date]

        logger.info(f"dataframe length: {len(d)}")

        if d.empty:
            continue

        # write to file
        out_path = os.path.join(output, date + "." + format)

        logger.info(f"writing to file: {out_path}")

        if format == "csv":
            d.to_csv(out_path, index=False, sep=sep)
        elif format == "json":
            d.to_json(out_path, index=False)
        else:
            raise ValueError(
                f"format {format} is not supported in write_df_by_date function"
            )
