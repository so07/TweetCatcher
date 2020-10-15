import argparse

from .tweet_unique import tweet_unique
from .tweet_utils import logger, set_logging_verbosity, write_df_by_date
from .clargs import (
    add_parser_debug,
    add_parser_date,
    add_parser_format,
    add_parser_input,
    add_parser_output,
)


def main():

    parser = argparse.ArgumentParser(
        prog="tweet_unique",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    add_parser_input(parser)
    add_parser_output(parser)
    add_parser_date(parser)
    add_parser_format(parser)
    add_parser_debug(parser)

    parser.add_argument(
        "--reference-path",
        "-r",
        dest="reference_path",
        required=True,
        help=f"reference to check for duplicates",
    )

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    df = tweet_unique(
        args.search_path, args.search_pattern, args.reference_path, args.verbose,
    )

    write_df_by_date(df, args.output, format=args.format, sep=args.separator)


if __name__ == "__main__":
    main()
