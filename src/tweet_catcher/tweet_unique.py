import numpy as np

from .tweet_utils import logger, read_csv
from .tweet_cleaner import remove_duplicates


def unique_tweets(df, ref_df):

    # get unique ids
    logger.debug(f"get unique ids")
    ids = df.id.unique()
    ref_ids = ref_df.id.unique()

    # compare ids
    unique_ids = np.setdiff1d(ids, ref_ids)

    # filter dataframe
    df = df[df["id"].isin(unique_ids)]

    logger.info(f"tweets after unique: {len(df)}")

    return df


def tweet_unique(
    path, pattern, reference_path, reference_pattern, verbose=0, dry_run=False
):

    # read dataset
    df = read_csv(path, pattern, dry_run=dry_run)

    if df.empty and not dry_run:
        logger.info("read empty dataframe")
        return df

    # remove duplicates
    if not dry_run:
        df = remove_duplicates(df)

    # read reference dataset
    ref_df = read_csv(reference_path, reference_pattern, dry_run=dry_run)

    if not dry_run:
        df = unique_tweets(df, ref_df)

    if df.empty and not dry_run:
        logger.info("empty dataframe after unique")
        return df

    return df
