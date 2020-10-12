import argparse

from .tweet_converter import tweet_converter
from .tweet_utils import logger, set_logging_verbosity, write_df_by_date
from .clargs import add_parser_debug, add_parser_date


def main():

    parser = argparse.ArgumentParser(
        prog="tweet_converter",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    add_parser_date(parser)
    add_parser_debug(parser)

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

    parser.add_argument(
        "--format",
        "-f",
        dest="format",
        default="json",
        choices=["json", "csv"],
        help="output file format. (default %(default)s)",
    )

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    df = tweet_converter(args.search_path, args.search_pattern, args.verbose,)

    write_df_by_date(df, args.output, format=args.format)


if __name__ == "__main__":
    main()
