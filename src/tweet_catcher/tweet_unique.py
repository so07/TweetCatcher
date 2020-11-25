import numpy as np

from .tweet_utils import logger, read_csv, empty_df
from .tweet_cleaner import remove_duplicates


def unique_tweets(df, ref_df, report_only=False):

    # get unique ids
    logger.debug(f"get unique ids")
    ids = df.id.unique()
    ref_ids = ref_df.id.unique()

    # compare ids
    logger.debug(f"compare ids")
    logger.debug(f" tweets {len(ids)}")
    logger.debug(f" refer. {len(ref_ids)}")
    unique_ids = np.setdiff1d(ids, ref_ids)

    if report_only:
        logger.info("report duplicate")
        num_tweets = len(ids)
        num_reference = len(ref_ids)
        num_unique = len(unique_ids)
        num_duplicate = num_tweets - num_unique
        logger.info(f"num tweets     {num_tweets}")
        logger.info(f"num reference  {num_reference}")
        logger.info(f"num unique     {num_unique}")
        logger.info(f"num duplicate  {num_duplicate}")
        return empty_df()

    logger.info(f"tweets before unique: {len(df)}")

    # filter dataframe
    df = df[df["id"].isin(unique_ids)]

    logger.info(f"tweets after unique: {len(df)}")

    return df


def tweet_unique(
    path,
    pattern,
    reference_path,
    reference_pattern,
    report_only=False,
    verbose=0,
    dry_run=False,
):

    # read dataset
    logger.info("reading dataset to unique")
    df = read_csv(path, pattern, dry_run=dry_run)

    if df.empty and not dry_run:
        logger.info("read empty dataframe")
        return df

    # remove duplicates
    if not dry_run:
        df = remove_duplicates(df)

    # read reference dataset
    logger.info("reading reference dataset")
    ref_df = read_csv(reference_path, reference_pattern, dry_run=dry_run)

    if not dry_run:
        df = unique_tweets(df, ref_df, report_only)

    if df.empty and not dry_run:
        logger.info("empty dataframe after unique")
        return df

    return df
