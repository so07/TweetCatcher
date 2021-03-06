import argparse

from .tweet_catcher import tweet_catcher
from .tweet_utils import logger, set_logging_verbosity
from .clargs import add_parser_debug, add_parser_date
from .clargs import add_parser_debug, add_parser_date, add_parser_output


def main():

    parser = argparse.ArgumentParser(
        prog="tweet_catcher",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    add_parser_output(parser)
    add_parser_date(parser)
    add_parser_debug(parser)

    parser.add_argument(
        "--pattern",
        "-p",
        dest="pattern",
        # required=True,
        help="search pattern for tweets",
    )

    parser.add_argument(
        "--user",
        "-u",
        dest="user",
        # required=True,
        default=None,
        help="twitter user name",
    )

    parser.add_argument(
        "--sleep" "-s",
        dest="sleep",
        default=0,
        help="interval in seconds between multiple download. (default %(default)s)",
    )

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    tweet_catcher(
        args.pattern,
        args.user,
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
