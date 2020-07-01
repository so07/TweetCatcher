import os
import glob
import logging
import datetime
import pandas as pd

logger = logging.getLogger()


def set_logging_verbosity(verbose):
    level = logging.INFO

    if verbose:
        level = logging.DEBUG

    logging.basicConfig(level=level)


def make_dir(directory):
    if not os.path.exists(directory):
        logger.info(f"make dir: {directory}")
        os.makedirs(directory)


def read_csv(path, pattern="*", extension="csv"):

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
        d = pd.read_csv(f)
        logger.debug(f"dataframe length: {len(d)}")
        df = pd.concat([df, d])

    # convert date in datetime.date

    #df.date = pd.to_datetime(df.date, format="%Y-%m-%d")
    #df.time = pd.to_datetime(df.time, format="%H:%M:%S")

    logger.info(f"dataframe length: {len(df)}")

    logger.debug(df.columns)

    return df


def write_df_by_date(df, output):
    logger.debug(f"output directory: {output}")
    make_dir(output)

    daterange = pd.date_range(df.date.min(), df.date.max(), freq="1D")

    for i in daterange:
        date = str(i.date())

        logger.debug(f"analize date: {date}")

        # select df by date
        d = df[ df.date == date ]

        # write to file
        out_path = os.path.join(output, date + ".csv")
        logger.info(f"writing to file: {out_path}")
        logger.info(f"dataframe length: {len(d)}")
        d.to_csv(out_path)


