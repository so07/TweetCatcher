import re
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
    """remove tweets duplicated.
    compare tweet ids."""

    logger.info(f"remove duplicate")

    ids = df.id.unique()

    logger.debug(f"unique ids: {len(ids)}")

    # remove duplicates
    df.drop_duplicates(inplace=True)

    logger.info(f"tweets after removing duplicates: {len(df)}")

    return df


def language_filter(df, lang):
    """filter tweets by language."""

    def check_lang(row):
        text = row.tweet
        # logger.debug(f"tweet: {text}")

        try:
            if detect(text) == lang:
                return True
        except:
            pass

        return False

    logger.info(f"filter by language {lang}")

    mask = df.apply(check_lang, axis=1)

    df = df[mask]

    logger.info(f"tweets after filter by language: {len(df)}")

    return df


def emoji_filter(df):

    # https://stackoverflow.com/a/49146722/330558
    def remove_emoji(string):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", string)

    def check_empty_tweet(row):
        text = row.tweet
        if text.isspace() or not text:
            return False
        return True

    df["tweet"] = df["tweet"].apply(remove_emoji)

    # remove empty tweet
    mask = df.apply(check_empty_tweet, axis=1)
    df = df[mask]

    return df


def tweet_cleaner(
    path,
    pattern=None,
    lang=None,
    verbose=0,
    refine=False,
    remove_emoticons=False
):

    # read dataset
    df = read_csv(path, pattern)

    if df.empty:
        logger.info("empty dataframe")
        return df

    # remove duplicates
    df = remove_duplicates(df)

    # remove emoticons
    if remove_emoticons:
        df = emoji_filter(df)

    # remove empty line
    logger.info("remove empty lines")
    df = df.replace(r"\n", " ", regex=True)

    # language filter
    if lang is not None:
        df = language_filter(df, lang)

    if refine:
        # remove useless columns
        keys_to_remove = [
            "mentions",
            "urls",
            "reply_to",
        ]
        logger.info(f"remove useless entry: {keys_to_remove}")
        df = df.drop(keys_to_remove, axis=1)

    logger.info(f"tweets after cleaner: {len(df)}")

    return df
