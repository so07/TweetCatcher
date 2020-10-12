import ast
from langdetect import detect

from .tweet_utils import logger, set_logging_verbosity, read_csv


def get_hashtags(df):
    h = set()
    for i in df.hashtags.tolist():
        h.update(ast.literal_eval(i))
    h = list(h)
    h.sort()
    return h


def remove_duplicates(df):
    """remove duplicates from dataframe.
       compare twitter ids."""

    ids = df.id.unique()
    logger.debug(f"unique ids: {len(ids)}")

    # remove duplicates
    df.drop_duplicates(inplace=True)
    logger.info(f"dataframe length after removing duplicates: {len(df)}")

    return df


def language_filter(df, lang):
    """filter twitter by language."""

    def check_lang(row):
        if detect(row.tweet) == lang:
            return True
        return False

    mask = df.apply(check_lang, axis=1)

    return df[mask]


def tweet_cleaner(
    path, pattern=None, lang=None, verbose=0,
):

    # read dataset
    df = read_csv(path, pattern)

    # remove duplicates
    df = remove_duplicates(df)

    # language filter
    if lang is not None:
        df = language_filter(df, lang)

    return df
