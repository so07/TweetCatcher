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


def empty_df():
    return pd.DataFrame()


def read_csv(path, pattern="*", extension="csv", dry_run=False):
    """read csv file and return pandas dataframe"""

    # file pattern
    file_pattern = "*"
    if pattern:
        file_pattern = pattern
    file_pattern += "." + extension

    logger.debug(f"file patter: {file_pattern}")

    if not isinstance(path, list):
        path = [path]

    logger.debug(f"file path: {path}")

    # list of files
    ls = []
    for p in path:
        ls.extend(glob.glob(os.path.join(p, file_pattern)))
    # sort files
    ls = sorted(ls)

    logger.debug(f"Found {len(ls)} files")
    logger.debug(" ".join(ls))

    # read files

    df = pd.DataFrame()

    for f in ls:
        logger.debug(f"reading file: {f}")

        sep = sniff_sep(f)
        logger.debug(f"csv separator: {sep}")

        if not dry_run:
            d = pd.read_csv(f, sep=sep, dtype=str)
            logger.debug(f"dataframe length: {len(d)}")

            df = pd.concat([df, d])

    # convert date in datetime.date

    # df.date = pd.to_datetime(df.date, format="%Y-%m-%d")
    # df.time = pd.to_datetime(df.time, format="%H:%M:%S")

    logger.info(f"tweets: {len(df)}")

    logger.debug(df.columns)

    return df


def write_df_by_date(df, output, prefix="", format="csv", sep=",", dry_run=False):
    logger.debug("@write_df_by_date")

    if df.empty and not dry_run:
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

        # base name for file
        if not prefix:
            base_name = ""
        else:
            base_name = prefix + "-"
        base_name += date

        # write to file
        out_path = os.path.join(output, base_name + "." + format)

        logger.info(f"writing to file: {out_path}")

        if format == "csv":
            d.to_csv(out_path, index=False, sep=sep)
        elif format == "json":
            d.to_json(out_path, index=False)
        else:
            raise ValueError(
                f"format {format} is not supported in write_df_by_date function"
            )
