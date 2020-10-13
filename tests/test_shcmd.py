"""
unit tests for TweetCatcher module
"""

from datetime import datetime

from tweet_catcher import tweet_catcher


def test_import():
    """test import module"""
    import tweet_catcher
    from tweet_catcher.tweet_catcher import tweet_catcher
    from tweet_catcher.tweet_cleaner import tweet_cleaner
    from tweet_catcher.tweet_converter import tweet_converter


def test_import2():
    from tweet_catcher import tweet_catcher
    from tweet_catcher import tweet_cleaner
    from tweet_catcher import tweet_converter


def test_create_file(tmpdir):
    print(tmpdir)
    tweet_catcher(
        "MickJagger",
        datetime.strptime("2014-12-31 23:00:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime("2015-01-01 01:00:00", "%Y-%m-%d %H:%M:%S"),
        tmpdir,
    )
