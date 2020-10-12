import ast

from .catcher_utils import logger, set_logging_verbosity, read_csv


def get_hashtags(df):
    h = set()
    for i in df.hashtags.tolist():
        h.update(ast.literal_eval(i))
    h = list(h)
    h.sort()
    return h


def remove_duplicates(df):

    ids = df.id.unique()
    logger.debug(f"unique ids: {len(ids)}")

    # remove duplicates
    df.drop_duplicates(inplace=True)
    logger.info(f"dataframe length after removing duplicates: {len(df)}")

    return df


def tweet_cleaner(
    path, pattern=None, verbose=0,
):

    # read dataset
    df = read_csv(path, pattern)

    # remove duplicates
    df = remove_duplicates(df)

    return df
