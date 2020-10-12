import argparse

from .tweet_catcher import tweet_catcher
from .catcher_utils import logger, set_logging_verbosity
from .clargs import add_parser_debug, add_parser_date


def main():

    parser = argparse.ArgumentParser(
        prog="tweet_catcher",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--pattern",
        "-p",
        dest="pattern",
        required=True,
        help="search pattern for tweets",
    )

    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        default="tweet_search",
        help="directory where tweet data are stored. (default %(default)s)",
    )

    add_parser_date(parser)

    parser.add_argument(
        "--sleep",
        "-s",
        dest="sleep",
        default=0,
        help="interval in seconds between multiple download. (default %(default)s)",
    )

    add_parser_debug(parser)

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    tweet_catcher(
        args.pattern,
        args.from_date,
        args.to_date,
        args.output,
        args.freq[0],
        args.freq[1],
        sleep=args.sleep,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
