import ast

from .tweet_utils import logger, set_logging_verbosity, read_csv


def tweet_converter(
    path,
    pattern=None,
    verbose=0,
):

    # read dataset
    df = read_csv(path, pattern)

    return df
