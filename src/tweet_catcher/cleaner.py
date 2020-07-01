import argparse

from .tweet_cleaner import tweet_cleaner
from .catcher_utils import logger, set_logging_verbosity, write_df_by_date
from .clargs import add_parser_debug, add_parser_date

def main():
    #read_csv("/home/sergio/tweet_tmp827/old/covid")
    #read_csv("/home/sergio/tweet_tmp827/old/covid", "covid-19_2020-01-20")

    parser = argparse.ArgumentParser(
        prog="tweet_cleaner",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    add_parser_debug(parser)
    add_parser_date(parser)

    parser.add_argument(
        "--path",
        "-p",
        dest="search_path",
        default="tweet_search",
        help="directory where search csv file with tweets. (default %(default)s)",
    )

    parser.add_argument(
        "--pattern",
        "-P",
        dest="search_pattern",
        default=None,
        help="pattern of csv file to clean. (default %(default)s)",
    )

    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        default="tweet_clean",
        help="directory where clean tweet data are stored. (default %(default)s)",
    )

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    df = tweet_cleaner(
        args.search_path,
        args.search_pattern,
        args.verbose,
            )

    write_df_by_date(
            df,
            args.output)

if __name__ == "__main__":
    main()

